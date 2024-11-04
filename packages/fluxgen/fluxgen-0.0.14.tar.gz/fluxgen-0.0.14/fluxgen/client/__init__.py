#!/usr/bin/env python

import argparse
import sys

import fluxgen


def get_parser():
    parser = argparse.ArgumentParser(
        description="Fluxgen Python",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--version",
        dest="version",
        help="show software version.",
        default=False,
        action="store_true",
    )

    description = "actions for Fluxgen"
    subparsers = parser.add_subparsers(
        help="actions",
        title="actions",
        description=description,
        dest="command",
    )

    # print version and exit
    subparsers.add_parser("version", description="show software version")

    # Write the install and configuration script
    create = subparsers.add_parser(
        "create",
        description="create an install and configuration script for flux",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    create.add_argument(
        "--brokers",
        help="Brokers, either short hand or comma separated",
    )
    create.add_argument(
        "--linkname",
        help="Device name (e.g., eth0)",
        default="eth0",
    )
    create.add_argument(
        "--subdomain",
        help="Subdomain for the workers (e.g., m.default.svc.cluster.local)",
    )
    create.add_argument(
        "--outfile",
        help="Name for install file (defaults to flux-install.sh)",
        default="flux-install.sh",
    )
    create.add_argument(
        "--dry-run",
        help="Preview the install script (don't write to file)",
        default=False,
        action="store_true",
    )
    create.add_argument(
        "--lead-broker",
        help="Is this the lead broker?",
        default=False,
        action="store_true",
    )
    return parser


def run_fluxgen():
    parser = get_parser()

    def help(return_code=0):
        version = fluxgen.__version__

        print("\nFluxgen Python v%s" % version)
        parser.print_help()
        sys.exit(return_code)

    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        help()

    # If an error occurs while parsing the arguments, the interpreter will exit with value 2
    args, command = parser.parse_known_args()

    # Show the version and exit
    if args.command == "version" or args.version:
        print(fluxgen.__version__)
        sys.exit(0)

    # retrieve subparser (with help) from parser
    helper = None
    subparsers_actions = [
        action for action in parser._actions if isinstance(action, argparse._SubParsersAction)
    ]
    for subparsers_action in subparsers_actions:
        for choice, subparser in subparsers_action.choices.items():
            if choice == args.command:
                helper = subparser
                break

    # Does the user want a shell?
    if args.command == "create":
        from .create import main

    # Pass on to the correct parser
    return_code = 0
    try:
        main(args=args, parser=parser, command=command, subparser=helper)
        sys.exit(return_code)
    except UnboundLocalError:
        return_code = 1
    help(return_code)


if __name__ == "__main__":
    run_fluxgen()
