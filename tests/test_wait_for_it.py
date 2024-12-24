import http.server
import shlex
import socket
import socketserver
from subprocess import Popen, PIPE
import os
import threading
import pytest

MISSING_ARGS_TEXT = "Error: you need to provide a url to test."
HELP_TEXT = "Usage:"  # Start of help text
DIVIDE_LINE = '-'*71  # Output line of dashes

def execute(cmd):
    """Executes a command and returns exit code, STDOUT, STDERR"""
    args = shlex.split(cmd)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    return exitcode, out.decode('utf-8'), err.decode('utf-8')

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def start_http_server(port):
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    return httpd

@pytest.fixture
def wait_script():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    wait_for_it_path = os.path.join(script_dir, '../wait-for-it.sh')
    return wait_for_it_path

def test_no_args(wait_script):
    """Check that no arguments returns the missing args text and the correct return code"""
    exitcode, out, err = execute(wait_script)
    assert exitcode == 1
    assert err.startswith(MISSING_ARGS_TEXT)


def test_help(wait_script):
    """Check that help text is printed with --help argument"""
    exitcode, out, err = execute(f"{wait_script} --help")
    assert exitcode == 1
    assert err.startswith(HELP_TEXT)


def test_url(wait_script):
    """Check that --host and --port args work correctly"""
    port = get_free_port()
    timeout = 3
    httpd = start_http_server(port)

    try :
        exitcode, out, err = execute(f"{wait_script} --url=http://localhost:{port} --timeout={timeout}")
        assert exitcode == 0
        assert f"wait-for-it.sh: waiting {timeout} seconds for http://localhost:{port}" in err
    finally:
        httpd.shutdown
