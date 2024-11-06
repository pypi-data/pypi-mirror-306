# -*- coding: utf-8 -*-
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/g-inspector for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import json
import os
from pathlib import Path

import pytest
from commoncode.testcase import FileDrivenTesting
from scancode.cli_test_utils import check_json
from scancode.cli_test_utils import check_json_scan
from scancode.cli_test_utils import run_scan_click
from scancode_config import REGEN_TEST_FIXTURES

from go_inspector.binary import _collect_go_package_from_data
from go_inspector.binary import collect_and_parse_symbols
from go_inspector.binary import collect_go_package

test_env = FileDrivenTesting()
test_env.test_data_dir = os.path.join(os.path.dirname(__file__), "data")


def test_collect_and_parse_symbols_with_plain_windows_exe():
    go_binary = test_env.get_test_loc("plain_windows.exe")
    with pytest.raises(Exception):
        collect_and_parse_symbols(go_binary)


def test_collect_and_parse_symbols_with_plain_elf():
    go_binary = test_env.get_test_loc("plain_arm_gentoo_elf")
    with pytest.raises(Exception):
        collect_and_parse_symbols(go_binary)


@pytest.mark.parametrize(
    "exe_path",
    [
        "basic/app_lin_exe",
        "basic/app_mac_exe",
        "basic/app_win_exe",
        "basic/app_lin_exe_stripped",
    ],
)
def test_collect_and_parse_symbols_with_mini_go_app_linux(exe_path):
    go_binary = test_env.get_test_loc(exe_path)
    expected = f"{go_binary}-collect_and_parse_symbols.json"
    results = collect_and_parse_symbols(go_binary)
    check_json(expected, results, regen=REGEN_TEST_FIXTURES)


def test_collect_and_parse_symbols_with_large_go_app_linux():
    go_binary = Path(test_env.test_data_dir).parent.parent / "src/go_inspector/bin/GoReSym_lin"
    expected = test_env.get_test_loc(
        f"GoReSym_lin-collect_and_parse_symbols.json", must_exist=False
    )
    results = collect_and_parse_symbols(go_binary)
    check_json(expected, results, regen=REGEN_TEST_FIXTURES)


def test_scancode_plugin_with_go_symbol_option():
    test_file = test_env.get_test_loc("basic/app_lin_exe", copy=True)
    result_file = test_env.get_temp_file("json")
    args = ["--go-symbol", test_file, "--json", result_file]
    run_scan_click(args)
    expected = test_env.get_test_loc("basic/app_lin_exe-scancode.expected.json", must_exist=False)
    check_json_scan(expected, result_file, regen=REGEN_TEST_FIXTURES)


def test_collect_go_package_with_large_go_app_linux():
    go_binary = Path(test_env.test_data_dir).parent.parent / "src/go_inspector/bin/GoReSym_lin"
    expected = test_env.get_test_loc("packages/GoReSym_lin-expected.json", must_exist=False)
    results = [p.to_dict() for p in collect_go_package(location=go_binary)]
    check_json(expected, results, regen=REGEN_TEST_FIXTURES)


def test_collect_go_package_from_data_with_large_go_app_linux():
    with open(test_env.get_test_loc("packages/otelcol-contrib.exe.json")) as gbd:
        go_binary_data = json.load(gbd)
    expected = test_env.get_test_loc("packages/otelcol-contrib.exe-expected.json", must_exist=False)
    results = [
        pd.to_dict()
        for pd in _collect_go_package_from_data(go_data=go_binary_data, location="some/fake/loc")
    ]
    check_json(expected, results, regen=REGEN_TEST_FIXTURES)


def test_collect_go_package_from_data_with_large_go_app_linux2():
    with open(test_env.get_test_loc("packages/tidb-server.json")) as gbd:
        go_binary_data = json.load(gbd)
    expected = test_env.get_test_loc("packages/tidb-server-expected.json", must_exist=False)
    results = [
        pd.to_dict()
        for pd in _collect_go_package_from_data(go_data=go_binary_data, location="some/fake/loc")
    ]
    check_json(expected, results, regen=REGEN_TEST_FIXTURES)
