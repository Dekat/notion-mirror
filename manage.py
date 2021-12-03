import argparse
from argparse import Namespace
from enum import Enum

from notion_mirror import logger
from notion_mirror.controllers.endpoints import app


class Command(Enum):
    run = "run"


def parse_args() -> Namespace:  # pragma: no cover
    parser = argparse.ArgumentParser(description="Manage this tool.")
    parser.add_argument(
        "command",
        metavar="CMD",
        type=str,
        choices=[c.value for c in Command],
        help="The command to execute",
    )
    args = parser.parse_args()
    logger.info(args)
    return args


def execute_command(args: Namespace) -> None:
    if args.command == Command.run.value:
        logger.info("Starting API server...")
        app.run(
            host="0.0.0.0",
            debug=app.config["FLASK_DEBUG"],
            port=app.config["FLASK_PORT"],
        )


if __name__ == "__main__":  # pragma: no cover
    execute_command(parse_args())
