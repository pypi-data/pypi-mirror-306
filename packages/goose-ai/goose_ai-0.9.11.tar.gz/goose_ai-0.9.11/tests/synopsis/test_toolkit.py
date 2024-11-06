import os
import pytest
from goose.synopsis.toolkit import SynopsisDeveloper
from goose.synopsis.system import system


class MockNotifier:
    def log(self, message):
        pass

    def status(self, message):
        pass


@pytest.fixture
def toolkit(tmpdir):
    original_cwd = os.getcwd()
    os.chdir(tmpdir)
    system.cwd = str(tmpdir)
    notifier = MockNotifier()
    toolkit = SynopsisDeveloper(notifier=notifier)

    yield toolkit

    # Teardown: cancel all processes and restore original working directory
    for process_id in list(system._processes.keys()):
        system.cancel_process(process_id)
    os.chdir(original_cwd)
    system.cwd = original_cwd


def test_shell(toolkit, tmpdir):
    result = toolkit.bash(command="echo 'Hello, World!'")
    assert "Hello, World!" in result


def test_text_editor_read_write_file(toolkit, tmpdir):
    test_file = tmpdir.join("test_file.txt")
    content = "Test content"

    toolkit.text_editor(command="create", path=str(test_file), file_text=content)
    assert test_file.read() == content

    result = toolkit.text_editor(command="view", path=str(test_file))
    assert "Displayed content of" in result
    assert system.is_active(str(test_file))


def test_text_editor_patch_file(toolkit, tmpdir):
    test_file = tmpdir.join("test_file.txt")
    test_file.write("Hello, World!")

    toolkit.text_editor(command="view", path=str(test_file))  # Remember the file
    result = toolkit.text_editor(command="str_replace", path=str(test_file), old_str="World", new_str="Universe")
    assert "Successfully replaced before with after" in result
    assert test_file.read() == "Hello, Universe!"


def test_change_dir(toolkit, tmpdir):
    subdir = tmpdir.mkdir("subdir")
    result = toolkit.bash(working_dir=str(subdir))
    assert str(subdir) in result
    assert system.cwd == str(subdir)


def test_start_process(toolkit, tmpdir):
    process_id = toolkit.process_manager(command="start", shell_command="python -m http.server 8000")
    assert process_id > 0

    # Check if the process is in the list of running processes
    processes = toolkit.process_manager(command="list")
    assert process_id in processes
    assert "python -m http.server 8000" in processes[process_id]


def test_list_processes(toolkit, tmpdir):
    process_id1 = toolkit.process_manager(command="start", shell_command="python -m http.server 8001")
    process_id2 = toolkit.process_manager(command="start", shell_command="python -m http.server 8002")

    processes = toolkit.process_manager(command="list")
    assert process_id1 in processes
    assert process_id2 in processes
    assert "python -m http.server 8001" in processes[process_id1]
    assert "python -m http.server 8002" in processes[process_id2]


def test_cancel_process(toolkit, tmpdir):
    process_id = toolkit.process_manager(command="start", shell_command="python -m http.server 8003")

    result = toolkit.process_manager(command="cancel", process_id=process_id)
    assert result == f"Process {process_id} cancelled"

    # Verify that the process is no longer in the list
    processes = toolkit.process_manager(command="list")
    assert process_id not in processes


def test_fetch_web_content(toolkit):
    url = "http://example.com"

    result = toolkit.fetch_web_content(url)
    assert "html_file_path" in result
    assert "text_file_path" in result

    html_file_path = result["html_file_path"]
    text_file_path = result["text_file_path"]

    with open(html_file_path, "r") as html_file:
        fetched_content = html_file.read()

    assert "Example Domain" in fetched_content

    with open(text_file_path, "r") as html_file:
        fetched_content = html_file.read()
    assert "Example Domain" in fetched_content
