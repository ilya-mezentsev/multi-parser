from dataclasses import dataclass

import argparse


__all__ = [
    'cli_arguments',
    'CLISettings',
]


@dataclass
class CLISettings:
    mode: str
    resources_path: str
    logging_level: str


def cli_arguments() -> CLISettings:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--mode',
        type=str,
        help='App mode (web/telegram)',
    )

    parser.add_argument(
        '--resources-path',
        type=str,
        help='Path to resources file',
    )

    parser.add_argument(
        '--logging-level',
        type=str,
        help='Logging level',
    )

    args = parser.parse_args()

    return CLISettings(
        mode=args.mode,
        resources_path=args.resources_path,
        logging_level=args.logging_level,
    )
