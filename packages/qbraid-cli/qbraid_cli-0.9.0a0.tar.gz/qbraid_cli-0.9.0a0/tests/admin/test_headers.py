# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Unit tests for the `qbraid_cli.admin.app` module's `headers` command.

"""
import os
import re

from typer.testing import CliRunner

from qbraid_cli.admin.app import admin_app
from qbraid_cli.admin.headers import DEFAULT_HEADER, get_formatted_header

runner = CliRunner()


def _get_test_file_path(test_type: str) -> str:
    return os.path.join(os.path.dirname(__file__), f"test_{test_type}.py")


def _get_test_file(test_type: str) -> str:
    # construct the file name
    file_path = _get_test_file_path(test_type)

    if test_type == "no_header":
        with open(file_path, "w") as f:
            f.write("print('hello world')")
    elif test_type == "correct_header":
        with open(file_path, "w") as f:
            f.write(DEFAULT_HEADER + "\n\n" + "print('hello world')")
    elif test_type == "old_header":
        with open(file_path, "w") as f:
            f.write("# This is an old header\n\n" + "print('hello world')")
    else:
        raise ValueError(f"Invalid test type: {test_type}")

    return file_path


def _remove_test_file(test_type: str) -> None:
    file_path = _get_test_file_path(test_type)
    os.remove(file_path)


def strip_ansi_codes(text):
    ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", text)


def _verify_result(result, expected_exit_code: int, expected_output: str):
    assert expected_output in strip_ansi_codes(result.stdout)
    assert result.exit_code == expected_exit_code


def test_header_fix_for_file_with_correct_header():
    """Test that the header fix function does not change the file with the correct header."""
    file_path = _get_test_file("correct_header")
    original_content = open(file_path, "r").read()

    result = runner.invoke(admin_app, [file_path, "--fix"])

    _verify_result(result, 0, "1 file left unchanged")

    # assert that the file has not been changed
    with open(file_path, "r") as f:
        assert f.read() == original_content

    _remove_test_file("correct_header")


def test_header_fix_for_file_with_no_header():
    """Test that the header fix function adds the new header to a file with no header."""
    file_path = _get_test_file("no_header")

    result = runner.invoke(admin_app, [file_path, "--fix"])

    _verify_result(result, 0, "1 file fixed")

    # assert that the file has the new header
    with open(file_path, "r") as f:
        assert f.read() == DEFAULT_HEADER + "\n" + "print('hello world')"

    _remove_test_file("no_header")


def test_header_update_for_file_with_old_header():
    """Test that the header fix function updates the header in a file with an old header."""
    file_path = _get_test_file("old_header")

    result = runner.invoke(admin_app, [file_path, "--fix", "-t", "gpl", "-p", "test_project"])

    _verify_result(result, 0, "1 file fixed")

    # assert that the file has the new header
    with open(file_path, "r") as f:
        assert (
            f.read() == get_formatted_header("gpl", "test_project") + "\n" + "print('hello world')"
        )

    _remove_test_file("old_header")


def test_files_in_directory():
    """Test that all files in a directory are fixed."""
    test_files = ["no_header", "correct_header", "old_header"]
    _ = [_get_test_file(test_file) for test_file in test_files]

    result = runner.invoke(admin_app, [os.path.dirname(__file__), "--fix"])

    _verify_result(result, 0, "2 files fixed")

    for test_file in test_files:
        _remove_test_file(test_file)


def test_invalid_path():
    """Test that the header fix function returns an error for an invalid path."""
    file_path = "invalid_path"

    result = runner.invoke(admin_app, [file_path, "--fix"])

    _verify_result(result, 2, f"Path '{file_path}' does not exist")


def test_invalid_header_types():
    """Test that the header fix function returns an error for invalid header types."""
    file_path = _get_test_file("no_header")

    result = runner.invoke(admin_app, [file_path, "--fix", "-t", "invalid_header"])
    _verify_result(result, 2, "Invalid value for '--type' / '-t'")
    _remove_test_file("no_header")


def test_correct_identification_of_bad_headers():
    """Test that the header fix function correctly identifies files with bad headers."""
    file_path = _get_test_file("old_header")

    result = runner.invoke(admin_app, [file_path])

    _verify_result(result, 1, "would fix")

    _remove_test_file("old_header")


def test_non_python_files_are_untouched():
    """Test that the header fix function does not change non-Python files."""
    non_python_file_path = os.path.join(os.path.dirname(__file__), "non_python_file.txt")

    with open(non_python_file_path, "w") as f:
        f.write("test")

    result = runner.invoke(admin_app, [non_python_file_path, "--fix"])

    _verify_result(result, 0, "No Python files present. Nothing to do")

    os.remove(non_python_file_path)
