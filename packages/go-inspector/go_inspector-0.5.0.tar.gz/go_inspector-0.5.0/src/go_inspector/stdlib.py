# -*- coding: utf-8 -*-
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/go-inspector for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

"""
Utilities to filter Go standard library packages.
See also https://github.com/golang/pkgsite/blob/87c415249864b5860acab46939f96affd52275f4/internal/stdlib/stdlib.go#L5
"""


# Top level directories in go:
STANDARDS = {
    "archive",
    "bufio",
    "builtin",
    "bytes",
    "cmp",
    "compress",
    "container",
    "context",
    "crypto",
    "database",
    "debug",
    "embed",
    "encoding",
    "errors",
    "expvar",
    "flag",
    "fmt",
    "go",
    "hash",
    "html",
    "image",
    "index",
    "io",
    "log",
    "maps",
    "math",
    "mime",
    "net",
    "os",
    "path",
    "plugin",
    "reflect",
    "regexp",
    "runtime",
    "slices",
    "sort",
    "strconv",
    "strings",
    "sync",
    "syscall",
    "testing",
    "text",
    "time",
    "unicode",
    "unsafe",
}


def is_standard_library(pkg_import, standards=STANDARDS):
    """
    Return True if a Go package import strings is for the standard Go library.

    For example:
    >>> is_standard_library("foo")
    False

    """
    if not isinstance(pkg_import, str):
        return False

    pkg_import = pkg_import.strip()
    if " " in pkg_import:
        _, _, pkg_import = pkg_import.partition(" ")

    packages = pkg_import.split("/")
    base_package = packages[0]
    return base_package in standards
