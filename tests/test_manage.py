from argparse import Namespace
from unittest.mock import MagicMock

from manage import Command, execute_command
from notion_mirror.controllers.endpoints import app


def test_run_server():
    app.run = MagicMock()

    execute_command(Namespace(command=Command.run.value))

    app.run.assert_called_once()
