#!/usr/bin/env python

import subprocess
from distutils.command.build import build as distutils_build
from distutils.errors import LibError

import setuptools
from setuptools.command.develop import develop as setuptools_develop


def run_native_build():
    exitcode, output = subprocess.getstatusoutput(["./build.sh"])
    print(output)
    if exitcode:
        raise LibError("Unable to build native")


class BuildNative(distutils_build):
    def run(self):
        self.execute(run_native_build, (), msg="Building native code")
        distutils_build.run(self)


class DevelopNative(setuptools_develop):
    def run(self):
        self.execute(run_native_build, (), msg="Building develop native code")
        setuptools_develop.run(self)


if __name__ == "__main__":
    setuptools.setup(cmdclass={"build": BuildNative, "develop": DevelopNative})
