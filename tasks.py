##########################################################################
# Copyright (c) 2010-2022 Robert Bosch GmbH
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0.
#
# SPDX-License-Identifier: EPL-2.0
##########################################################################

"""
Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""
import glob
import os
import platform
import shutil
import webbrowser
from pathlib import Path
from subprocess import (
    PIPE,
    STDOUT,
    CalledProcessError,
    Popen,
    TimeoutExpired,
    check_output,
)
from time import sleep
from typing import Union

from invoke import task

ROOT_DIR = Path(__file__).parent
TEST_DIR = ROOT_DIR / "tests"
COVERAGE_DIR = TEST_DIR / "coverage_report.html"
SOURCE_DIR = ROOT_DIR / "ask-your-datasheet"
DOCS_DIR = ROOT_DIR / "docs"
DOCS_BUILD_DIR = DOCS_DIR / "_build"
DOCS_INDEX = DOCS_BUILD_DIR / "index.html"
PYTHON_DIRS = [str(d) for d in [SOURCE_DIR, TEST_DIR]]

COPYRIGHT = """\
##########################################################################
# Copyright TBD
##########################################################################

"""


def _delete_files(
    file_name: Union[str, Path], root_dir: Union[str, Path] = None
) -> None:
    """Delete files which matches given pattern.

    :param file_name: file name as unix shell style wildcard.
      Examples: "../../Tools/*/*.gif"
    :param root_dir: root folder to start search from (optional)
    :raise OsError: when file can't be removed
    .. note:: Using the “**” pattern in large directory trees may consume an inordinate amount of time.
    """

    if isinstance(file_name, Path):
        file_name = str(file_name)
    search_path = os.path.join(root_dir, file_name) if root_dir else file_name

    for file in glob.iglob(search_path, recursive=True):
        if Path(file).is_file():
            os.remove(file)


def _delete_folders(
    folder_name: str | Path, root_dir: str | Path | None = None
) -> None:
    """Delete folders which matches given pattern.

    :param folder_name: folder name as unix shell style wildcard.
      Examples: "**/*__pycache__" for all folders named "__pycache__"
    :param root_dir: root folder to start search from (optional)

    .. note:: Using the “**” pattern in large directory trees may consume an inordinate amount of time.
    """

    if isinstance(folder_name, Path):
        folder_name = str(folder_name)
    search_path = os.path.join(root_dir, folder_name) if root_dir else folder_name

    for folder in glob.iglob(search_path, recursive=True):
        if Path(folder).is_dir():
            shutil.rmtree(folder)


@task
def test(c):
    """
    Run tests
    """
    pty = platform.system() == "Linux"
    c.run("coverage run -m pytest")
    c.run("coverage html")
    c.run("coverage xml")
    c.run("coverage report")


@task
def docs(c):
    """
    Generate documentation
    """
    clean_docs(c)
    c.run("sphinx-build -b html {} {}".format(DOCS_DIR, DOCS_BUILD_DIR))
    webbrowser.open(DOCS_INDEX.as_uri())


@task
def clean_docs(c):
    """
    Clean up files from documentation builds
    """
    _delete_folders(DOCS_BUILD_DIR)


@task
def clean_build(c):
    """
    Clean up files from package building
    """
    _delete_folders("build", root_dir=ROOT_DIR)
    _delete_folders("dist", root_dir=ROOT_DIR)
    _delete_folders(".eggs", root_dir=ROOT_DIR)
    _delete_folders("**/*.egg-info", root_dir=ROOT_DIR)
    _delete_files("**/*.egg", root_dir=ROOT_DIR)


@task
def clean_python(c):
    """
    Clean up python file artifacts
    """
    _delete_files("**/*.pyc", root_dir=ROOT_DIR)
    _delete_files("**/*.pyo", root_dir=ROOT_DIR)
    _delete_files("**/*~", root_dir=ROOT_DIR)
    _delete_folders("**/*__pycache__", root_dir=ROOT_DIR)


@task
def changelog(c):
    c.run("auto-changelog -u --template templates/changelog/changelog.jinja2")


@task
def clean_tests(c):
    """
    Clean up files from testing
    """
    _delete_folders("**/.pytest_cache", root_dir=ROOT_DIR)
    _delete_files(".coverage", root_dir=ROOT_DIR)
    _delete_files("tests/coverage_report.xml", root_dir=ROOT_DIR)
    _delete_files("*-unittest.log", root_dir=ROOT_DIR)
    shutil.rmtree(COVERAGE_DIR, ignore_errors=True)


@task(pre=[clean_build, clean_python, clean_tests, clean_docs])
def clean(c):
    """
    Runs all clean sub-tasks
    """
    pass


@task(pre=[clean])
def release(c):
    """
    Make a release of the python package to pypi
    """
    c.run(
        "poetry publish --repository roche-gitlab --no-interaction --build --username __token__ --password ${token}"
    )
