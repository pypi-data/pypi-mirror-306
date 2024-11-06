# -*- coding: utf-8 -*-
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/go-inspector for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import json
import logging
import os
from os.path import abspath
from os.path import dirname
from os.path import join
from pathlib import Path
from typing import NamedTuple

from commoncode import command
from commoncode import fileutils
from packageurl import PackageURL
from typecode import contenttype
from typecode.contenttype import get_type

from go_inspector import utils

"""
Extract symbols information from Go binaries using GoReSym.
"""
LOG = logging.getLogger(__name__)


def get_goresym_location():
    curr_dir = dirname(abspath(__file__))
    return join(curr_dir, "bin", "GoReSym_lin")


def parse_go_binary(location, args=("-nofuncs",)):
    """
    Return a mapping of data extracted from a Go binary file at ``location``.
    Return an empty mapping if there is no symbols or if this is not a binary.
    Raise exceptions on errors.
    """
    if not is_executable_binary(location):
        return {}

    goresym_args = list(args) + [location]
    goresym_temp_dir = fileutils.get_temp_dir()
    envt = {"TMPDIR": goresym_temp_dir}

    try:
        rc, stdo, err = command.execute(
            cmd_loc=get_goresym_location(),
            args=goresym_args,
            env=envt,
            to_files=True,
        )

        if rc != 0:
            raise Exception(open(stdo).read() + "\n\n" + open(err).read())

        with open(stdo) as syms:
            return json.load(syms)

    finally:
        fileutils.delete(goresym_temp_dir)


def collect_and_parse_symbols(location, include_stdlib=True, **kwargs):
    """
    Return a mapping of Go symbols of interest for the Go binary file at ``location``.
    Return an empty mapping if there is no symbols or if this is not a binary.
    Raise exceptions on errors.
    """
    go_data = parse_go_binary(location=location, args=("-p",))
    return _collect_and_parse_symbols_from_data(go_data, include_stdlib)


def _collect_and_parse_symbols_from_data(go_data, include_stdlib=True, **kwargs):
    """
    Return a mapping of Go symbols of interest for the mapping of Go binary of ``go_data``.
    Return an empty mapping if there is no symbols or if this is not a binary.
    Raise exceptions on errors.
    """
    if not go_data:
        return {}

    build_info = go_data.get("BuildInfo") or {}
    filter_stdlib = ()
    if not include_stdlib:
        filter_stdlib = ()

    files = filter_paths(go_data.get("Files") or [], filter_stdlib=filter_stdlib)
    return dict(go_symbols=dict(build_info=build_info, file_paths=files))


def collect_go_package(location, **kwargs):
    """
    Yield a Go PackageData found in the Go binary file at ``location``.
    Raise exceptions on errors.
    """
    go_data = parse_go_binary(location=location)
    return _collect_go_package_from_data(go_data, location=location)


def get_build_info(go_data):
    if not go_data or not "BuildInfo" in go_data:
        return

    build_info = go_data["BuildInfo"]
    if (
        not build_info.get("GoVersion")
        and not build_info.get("Path")
        and not build_info.get("Settings")
    ):
        return
    main = build_info.get("Main") or {}
    if not main.get("Path") and not main.get("Version") and not main.get("Sum"):
        return
    return build_info


def _collect_go_package_from_data(go_data, location, **kwargs):
    """
    Yield a Go PackageData found in the Go binary file ``go_data`` mapping extracted from
    ``location`` string. Raise exceptions on errors.
    """
    build_info = get_build_info(go_data)
    if not build_info:
        return

    package_data = get_main_package(build_info=build_info, location=location)
    # note that we do not keep Deps in extra data, hence the pop
    deps = build_info.pop("Deps", []) or []
    package_data.dependencies = list(collect_dependencies(deps))
    if goversion := build_info.get("GoVersion"):
        gp = PackageURL(type="github", namespace="golang", name="go", version=goversion).to_string()
        package_data.extra_data["go_runtime_purl"] = gp
    yield package_data


def collect_dependencies(deps):
    """
    Yield DependentPackage for each dependency
    """
    for dep in deps:
        if dep_purl := GoModule.from_data(go_data=dep):
            yield dep_purl.as_dependent_package()


def get_main_package(build_info, location):
    """
    Return PackageData for the main module or app extracted from a ``buildinfo`` mapping.

    The data has this shape::
        Path: github.com/NVIDIA/k8s-device-plugin/cmd/nvidia-device-plugin
        Main:
            Path: github.com/NVIDIA/k8s-device-plugin
            Version: (devel)
            Sum:
            Replace:
        Settings:
        -   Key: -ldflags
            Value: -s -w '-extldflags=-Wl,--export-dynamic -Wl,--unresolved-symbols=ignore-in-object-files'
                -X github.com/NVIDIA/k8s-device-plugin/internal/info.gitCommit=a044adb83781f2e672e1436d51dbd0f9bf8828d8
                -X github.com/NVIDIA/k8s-device-plugin/internal/info.version=a044adb8
        -   Key: vcs
            Value: git
        -   Key: vcs.revision
            Value: 94a24974ab345324db1a1489c924af4b89d2d0e9
    """
    from packagedcode import models

    extra_data = {"build_info": build_info}

    main_module = GoModule.from_data(go_data=build_info.get("Main"))
    module_path = build_info.get("Path") or ""

    is_synthetic = False
    if not main_module and not module_path:
        # create a synthetic, generic package using the executable filename as a name
        pathloc = Path(location).name
        pkg = models.PackageData(
            datasource_id="golang_binary",
            primary_language="Go",
            extra_data=extra_data,
        )
        purl = PackageURL(type="generic", name=pathloc, qualifiers=dict(path=location))
        pkg.set_purl(package_url=purl)

    elif main_module:
        pkg = main_module.as_package_data()
        pkg.extra_data.update(extra_data)
        # when present , the "module_path" points to the full binary path in the source tree
        if module_path.startswith(main_module.path):
            pkg.subpath = module_path.replace(main_module.path, "").strip("/")
        else:
            # we ignore the path (kept in extra data) and only use main
            pass

        module_path = main_module.path

    # here we have no main_module only a path and no version
    elif module_path:
        module = GoModule.from_data(go_data=dict(path=module_path))
        pkg = module.as_package_data()

    else:
        # this cannot happen
        pass

    # enhance the package version
    ld_path = ld_commit = None
    vcs_revision = None
    vcs_tool = None

    if settings := build_info.get("Settings"):
        extra_data["settins"] = settings
        for kv in settings:
            key = kv.get("Key")
            val = kv.get("Value")
            if not val:
                continue

            if key == "-ldflags":
                lds = collect_commit_from_ldflags(ldflags=val)
                if lds:
                    ld_path, ld_commit = lds

            elif key == "vcs.revision":
                vcs_revision = val
            elif key == "vcs":
                vcs_tool = val

    # replace pkg with a package built from ld_path ld_commit
    if ld_path and ld_commit and is_synthetic:
        gomod = GoModule.from_data(dict(Path=ld_path, Version=ld_commit))
        pkg = gomod.as_package_data()

    elif not pkg.version or pkg.version == "devel":
        # handle things such as "(devel)" version and empty version
        # use commit as version
        if ld_path == module_path and ld_commit:
            pkg.version = ld_commit

        elif vcs_tool == "git" and vcs_revision:
            pkg.version = vcs_revision

    for key, val in utils.get_urls(pkg.purl).items():
        setattr(pkg, key, val)

    return pkg


def is_macho(location):
    """
    Return True if the file at ``location`` is in macOS/Darwin's Mach-O format, otherwise False.
    """
    t = get_type(location)
    return t.filetype_file.lower().startswith("mach-o") or t.mimetype_file.lower().startswith(
        "application/x-mach-binary"
    )


def is_executable_binary(location):
    """
    Return True if the file at ``location`` is an executable binary.
    """
    if not os.path.exists(location):
        return False

    if not os.path.isfile(location):
        return False

    typ = contenttype.Type(location)

    if not (typ.is_elf or typ.is_winexe or is_macho(location=location)):
        return False

    return True


def filter_paths(paths, filter_stdlib=()):
    """
    Return a new cleaned, filtered list of ``paths`` removing duplicates, direvctories and fake
    paths. Optionally removes standard library paths if a ``filter_stdlib`` sequence of stdlib path
    prefixes is provided.
    """
    files = set(paths)
    files = [f for f in files if not is_fake_path(f)]
    files = filter_directories(files)
    if filter_stdlib:
        files = [f for f in files if not f.startswith(filter_stdlib)]
    files.sort()
    return files


def is_fake_path(path):
    """
    Return True if a ``path`` string is for a fake path injected by the linker or compiler in the binary.
    See:
    https://github.com/smoofra/elfutils/blob/53b6f190892c738f28840e7481a09c7ee19b6720/src/srcfiles.cxx#L160

    For example:
    >>> is_fake_path("<built-in>")
    True
    >>> is_fake_path("foo/bar/<builtin>")
    True
    >>> is_fake_path("<artificial>")
    True
    >>> is_fake_path("/artificial/asdasdas/adsd")
    False
    >>> is_fake_path("<foo-bar>")
    False
    >>> is_fake_path("/sdfsdfsdf<unknown>/zffd")
    True
    """
    fake_paths = (
        # GCC intrinsics
        "<built-in>",
        "<builtin>",
        # seen in Go and C++
        "<artificial>",
        # seen in Go
        "<unknown>",
        "<autogenerated>",
    )

    return isinstance(path, str) and any(fs in path for fs in fake_paths)


def filter_directories(paths):
    """
    Return a new list of ``paths`` removing any path to a directory, defined as all the parent
    paths of each path.

    For example::
    >>> paths = ["for/bar/baz/some.c", "for/bar/baz", "for/bar"]
    >>> filter_directories(paths)
    ['for/bar/baz/some.c']
    """
    dirs = set()
    paths = [Path(p) for p in paths]
    for pth in paths:
        dirs.update(pth.parents)
    return [str(pth) for pth in paths if pth not in dirs]


class GoModule(NamedTuple):
    path: str
    version: str
    go_sum: str
    replacing: "GoModule"

    def to_dict(self):
        return dict(
            path=self.path,
            version=self.version,
            go_sum=self.go_sum,
            replacing=self.replacing and self.replacing.to_dict() or None,
        )

    @classmethod
    def from_data(self, go_data):
        """
        Return a new GoModule built from a ``go_data`` package mapping. Or None.

        Mapping has this shape:
            Path: github.com/opencontainers/runc
            Version: v1.1.12
            Sum:
            Replace:
                Path: github.com/opencontainers/runc
                Version: v1.1.1-0.20240131200429-02120488a4c0
                Sum:
                Replace:
        """
        if not go_data:
            return

        path = go_data.get("Path") or ""
        if not path:
            return

        replacing = None
        replaced_by = go_data.get("Replace")
        if replaced_by:
            replaced_path = path
            replaced_version = go_data.get("Version") or ""
            replaced_sum = go_data.get("Sum") or None
            replacing = GoModule(
                path=replaced_path, version=replaced_version, go_sum=replaced_sum, replacing=None
            )

            path = replaced_by.get("Path") or ""
            version = replaced_by.get("Version") or ""
            go_sum = replaced_by.get("Sum") or None

        else:
            version = go_data.get("Version") or ""
            go_sum = go_data.get("Sum") or None

        # handle things such as "(devel)"
        version = version and version.strip("()")
        return GoModule(path=path, version=version, go_sum=go_sum, replacing=replacing)

    def update(self, **data):
        """
        Return a new updated GoModule using a ``data`` mapping.
        """
        current = self.to_dict()
        current.update(data)
        return GoModule(**current)

    def purl(self):
        return self.package_url().to_string()

    def package_url(self):
        return PackageURL(type="golang", name=self.path, version=self.version)

    def as_dependent_package(self):
        """
        Return a DependentPackage for this module.
        """
        from packagedcode import models

        extra_data = self.get_extra_data()

        return models.DependentPackage(
            purl=self.purl(),
            extracted_requirement=self.version,
            # TODO: this should be require!!
            scope="dependency",
            is_runtime=True,
            is_optional=False,
            is_pinned=True,
            extra_data=extra_data,
        )

    def get_extra_data(self):
        extra_data = {}
        if self.go_sum:
            extra_data["go_sum"] = self.go_sum

        if self.replacing:
            extra_data["replacing"] = self.replacing.to_dict()
        return extra_data

    def as_package_data(self):
        """
        Return a PackageData for this module.
        """
        from packagedcode import models

        pkg = models.PackageData(
            datasource_id="golang_binary",
            primary_language="Go",
            extra_data=self.get_extra_data(),
        )
        pkg.set_purl(self.purl())
        return pkg


def collect_commit_from_ldflags(ldflags):
    """
    Yield a truple of (path, commit) extracted from ``ldflags`` string or NOne.

    For instance::
        -s -w '-extldflags=-Wl,--export-dynamic -Wl,--unresolved-symbols=ignore-in-object-files'
        -X github.com/NVIDIA/k8s-device-plugin/internal/info.gitCommit=a044adb83781f2e672e1436d51dbd0f9bf8828d8
    """
    for item in (ldflags or "").split():
        if "gitCommit=" in item:
            path, _, commit = item.rpartition("gitCommit=")
            return path, commit


def get_go_binary_handler():
    from packagedcode import models

    class GolangBinaryHandler(models.DatafileHandler):
        """
        ScanCode handler for Go binary. We use the standard assemble AND this is "activated" with a
        conditional import in ScanCode Toolkit packagedcode.__init__.py
        """

        datasource_id = "golang_binary"
        # filetypes = tuple()
        default_package_type = "golang"
        default_primary_language = "Go"
        description = "Go binary"
        documentation_url = "https://github.com/nexB/go-inspector/"

        @classmethod
        def is_datafile(cls, location, filetypes=tuple(), _bare_filename=False):
            return is_executable_binary(location)

        @classmethod
        def parse(cls, location, package_only=False):
            """
            Yield a golang PackageData objects given a package data file at ``location``.
            """
            yield from collect_go_package(location)

    return GolangBinaryHandler
