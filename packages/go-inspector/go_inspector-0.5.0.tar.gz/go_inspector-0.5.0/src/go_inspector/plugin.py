# -*- coding: utf-8 -*-
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/go-inspector for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import logging

import attr
from commoncode.cliutils import SCAN_GROUP
from commoncode.cliutils import PluggableCommandLineOption
from plugincode.scan import ScanPlugin
from plugincode.scan import scan_impl

from go_inspector.binary import collect_and_parse_symbols

"""
Extract symbols information from Go binaries using GoReSym.
"""
logger = logging.getLogger(__name__)


@scan_impl
class GoSymbolScannerPlugin(ScanPlugin):
    """
    Scan a Go binary for symbols using GoReSym.
    """

    resource_attributes = dict(
        go_symbols=attr.ib(default=attr.Factory(dict), repr=False),
    )

    options = [
        PluggableCommandLineOption(
            ("--go-symbol",),
            is_flag=True,
            default=False,
            help="Collect Go symbols.",
            help_group=SCAN_GROUP,
            sort_order=100,
        ),
    ]

    def is_enabled(self, go_symbol, **kwargs):
        return go_symbol

    def get_scanner(self, **kwargs):
        return collect_and_parse_symbols
