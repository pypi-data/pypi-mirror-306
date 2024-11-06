# -*- coding: utf-8 -*-
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/go-inspector for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#
import re

from packageurl import PackageURL


def get_nsname(purl):
    if purl.namespace:
        nsname = f"{purl.namespace}/{purl.name}"
    else:
        nsname = purl.name
    return nsname


def repository_homepage_url(purl):
    nsname = get_nsname(purl)
    url = f"https://pkg.go.dev/{nsname}"
    if version := purl.version:
        url = f"{url}@{version}"
    return url


def get_vcs_segments(purl):
    nsname = get_nsname(purl)
    if nsname.startswith(("github", "gitlab")):
        segments = nsname.strip("/").split("/")
        if len(segments) >= 3:
            typ = segments[0]
            ns = segments[1]
            nm = segments[2]
            return typ, ns, nm


def get_vcs_based_urls(purl):
    urls = {}
    tnsn = get_vcs_segments(purl)
    if tnsn:
        typ, ns, nm = tnsn
        urls["vcs_url"] = f"git+https://{typ}.com/{ns}/{nm}.git"
        urls["homepage_url"] = f"https://{typ}.com/{ns}/{nm}"
        urls["bug_tracking_url"] = f"https://{typ}.com/{ns}/{nm}/issues"
        urls["code_view_url"] = f"https://{typ}.com/{ns}/{nm}"

    return urls


def source_purl(purl):
    """
    Return a source PURL string or None.
    """
    tnsn = get_vcs_segments(purl)
    if tnsn:
        typ, ns, nm = tnsn
        # strip trailing .com from github.com
        typ, _, _ = typ.partition(".")
        vrs = purl.version
        # only use commit for pseudo semver versions
        if vrs and (commit := extract_commit(vrs)):
            vrs = commit

        return PackageURL(type=typ, namespace=ns, name=nm, version=vrs).to_string()


def is_pseudo_version(version):
    """
    Return true if this is a "pseudo version".

    See https://go.dev/doc/modules/version-numbers

    For example::
    >>> version = "v0.0.0-20191222103121-ae1c48aa8615"
    >>> is_pseudo_version("v0.0.0-20191222103121-ae1c48aa8615")
    True
    >>> is_pseudo_version("v0.1.0-20191222103121-ae1c48aa8615")
    False
    >>> is_pseudo_version("v2.0.17-alpha-stream-batch-insert")
    False
    >>> is_pseudo_version("v0.0.    ")
    False
    """
    return version and version.startswith("v0.0.0-")


def extract_commit(version):
    """
    Extract and return a commit from a Go mod/sum pseudo version or None

    For example::
    >>> version = "v0.0.0-20191222103121-ae1c48aa8615"
    >>> extract_commit(version)
    'ae1c48aa8615'
    """
    if is_pseudo_version(version):
        return version.split("-")[-1]


def repository_download_url(purl):
    if version := purl.version:
        nsname = get_nsname(purl)
        ensname = escape_path(nsname)
        eversion = escape_path(version)
        return f"https://proxy.golang.org/cloud.google.com/go/monitoring/@v/v1.17.0.zip"


def create_pseudo_version(vcs_commit, vcs_time):
    """
    See example:
    https://proxy.golang.org/github.com/mandiant/!go!re!sym/@v/v0.0.0-20240610210609-128f46b1611a.zip

    Calling:
        https://proxy.golang.org/github.com/mandiant/!go!re!sym/@v/v0.0.0-00010101000000-128f46b1611a.zip
    returns:
        not found: github.com/mandiant/GoReSym@v0.0.0-00010101000000-128f46b1611a:
        invalid pseudo-version: does not match version-control timestamp (expected 20240610210609)
    Data we collect has this shape:
        {
            "Key": "vcs",
            "Value": "git"
        },
        {
            "Key": "vcs.revision",
            "Value": "128f46b1611a099678ae445776929b2d476ffed7"
        },
        {
            "Key": "vcs.time",
            "Value": "2024-06-10T21:06:09Z"
        },
        {
            "Key": "vcs.modified",
            "Value": "false"
        }

    vcs.time: "2024-06-10T21:06:09Z"
               2024 06 10 21 06 09
    """
    normalized_time = re.sub(r"\D", "", vcs_time)
    normalized_commit = vcs_commit[:12]
    pseudo_version = f"v0.0.0-{normalized_time}-{normalized_commit}"
    return pseudo_version


def parse_version(vers):
    """
    Return a tuple of (major, minor, patch) numeric version numbers.
    Return None if this is not a version or not a semver version

    Ignores rc and betas.  This is a semver once you remove the go prefix.

    For example:
    >>> parse_version("go1.0")
    (1, 0, 0)
    >>> parse_version("go1")
    (1, 0, 0)
    >>> parse_version("go1.22.2")
    (1, 22, 2)
    >>> parse_version("go2.22.2")
    (2, 22, 2)

    >>> parse_version("go1.0.0rc2")
    >>> parse_version("1")
    """
    if not isinstance(vers, str):
        return

    _, go, version = vers.strip().partition("go")
    if go != "go":
        return

    if not version.replace(".", "").isdigit():
        return

    segments = version.split(".")
    l = len(segments)
    minor = patch = 0
    if l == 1:
        major = segments[0]
    elif l == 2:
        major, minor = segments
    elif l == 3:
        major, minor, patch = segments
    else:
        return

    return int(major), int(minor), int(patch)


def get_urls(purl):
    """
    Return a mapping of URLs and related PURLs PackageData attributes inferred for this Go module purl.
    """
    if isinstance(purl, str):
        purl = PackageURL.from_string(purl)
    urls = {}
    urls["repository_homepage_url"] = repository_homepage_url(purl)
    if rdu := repository_download_url(purl):
        urls["repository_download_url"] = rdu
    if su := source_purl(purl):
        urls["source_packages"] = [su]
    urls.update(get_vcs_based_urls((purl)))
    return urls


def escape_path(path: str) -> str:
    """
    Return an case-encoded module path or version name.

    This is done by replacing every uppercase letter with an exclamation mark followed by the
    corresponding lower-case letter, in order to avoid ambiguity when serving from case-insensitive
    file systems.

    See https://golang.org/ref/mod#goproxy-protocol.
    """
    escaped_path = ""
    for c in path:
        if c >= "A" and c <= "Z":
            # replace uppercase with !lowercase
            escaped_path += "!" + chr(ord(c) + ord("a") - ord("A"))
        else:
            escaped_path += c
    return escaped_path
