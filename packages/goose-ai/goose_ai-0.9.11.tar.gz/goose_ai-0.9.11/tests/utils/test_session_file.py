import os
from pathlib import Path
from unittest.mock import patch

import pytest
from goose.utils.session_file import (
    is_empty_session,
    list_sorted_session_files,
    read_from_file,
    read_or_create_file,
    session_file_exists,
)


@pytest.fixture
def file_path(tmp_path):
    return tmp_path / "test_file.jsonl"


def test_read_from_file_non_existing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_from_file(tmp_path / "no_existing.json")


def test_read_from_file_non_jsonl_file(file_path):
    file_path.write_text("Hello World")
    with pytest.raises(RuntimeError):
        read_from_file(file_path)


def test_read_or_create_file_when_file_not_exist(tmp_path):
    file_path = tmp_path / "no_existing.json"

    assert read_or_create_file(file_path) == []
    assert os.path.exists(file_path)


def test_list_sorted_session_files(tmp_path):
    session_files_directory = tmp_path / "session_files_dir"
    session_files_directory.mkdir()
    file_names = ["file1", "file2", "file3"]
    created_session_files = [create_session_file(session_files_directory, file_name) for file_name in file_names]

    sorted_files = list_sorted_session_files(session_files_directory)
    assert sorted_files == {
        "file3": created_session_files[2],
        "file2": created_session_files[1],
        "file1": created_session_files[0],
    }


def test_list_sorted_session_without_session_files(tmp_path):
    session_files_directory = tmp_path / "session_files_dir"

    sorted_files = list_sorted_session_files(session_files_directory)
    assert sorted_files == {}


def test_session_file_exists_return_false_when_directory_does_not_exist(tmp_path):
    session_files_directory = tmp_path / "session_files_dir"
    assert not session_file_exists(session_files_directory)


def test_session_file_exists_return_false_when_no_session_file_exists(tmp_path):
    session_files_directory = tmp_path / "session_files_dir"
    session_files_directory.mkdir()
    assert not session_file_exists(session_files_directory)


def test_session_file_exists_return_true_when_session_file_exists(tmp_path):
    session_files_directory = tmp_path / "session_files_dir"
    session_files_directory.mkdir()
    create_session_file(session_files_directory, "session1")
    assert session_file_exists(session_files_directory)


def create_session_file(file_path, file_name) -> Path:
    file = file_path / f"{file_name}.jsonl"
    file.touch()
    return file


@patch("pathlib.Path.is_file", return_value=True, name="mock_is_file")
@patch("pathlib.Path.stat", name="mock_stat")
def test_is_empty_session(mock_stat, mock_is_file):
    mock_stat.return_value.st_size = 0
    assert is_empty_session(Path("empty_file.json"))


@patch("pathlib.Path.is_file", return_value=True, name="mock_is_file")
@patch("pathlib.Path.stat", name="mock_stat")
def test_is_not_empty_session(mock_stat, mock_is_file):
    mock_stat.return_value.st_size = 100
    assert not is_empty_session(Path("non_empty_file.json"))


@patch("pathlib.Path.is_file", return_value=False, name="mock_is_file")
def test_is_not_empty_session_file_not_found(mock_is_file):
    assert not is_empty_session(Path("file_not_found.json"))
