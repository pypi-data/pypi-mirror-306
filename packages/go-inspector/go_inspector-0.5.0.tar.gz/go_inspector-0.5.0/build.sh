#!/usr/bin/env bash
#
# Copyright (c) nexB Inc. http://www.nexb.com/ - All rights reserved.
#

set -e

base_name=GoReSym-3.0.1
GOOS=linux

if [ $(uname -m) == 'aarch64' ]; then
    GOARCH="arm64"
else
    GOARCH="amd64"
fi

cd lib-src/

rm -rf $base_name
tar -xf $base_name.tar.gz

cd $base_name/

echo Build GoReSym
go build && mv GoReSym GoReSym_lin
strip GoReSym_lin
cp GoReSym_lin ../../src/go_inspector/bin/
cd ..
echo Done building GoReSym

rm -rf $base_name/
