"""Command line interface."""

import argparse
import sys

from libcli import BaseCLI

from pathtree.pathtree import PathTree

__all__ = ["PathtreeCLI"]


class PathtreeCLI(BaseCLI):
    """Command line interface."""

    config = {
        # distribution name, not importable package name
        "dist-name": "rlane-pathtree",
    }

    # When used by another application, options are prefixed.
    # When used internally, options are not prefixed.
    prefix = None  # "pathtree"

    def init_parser(self) -> None:
        """Initialize argument parser."""

        self.ArgumentParser(
            prog=__package__,
            description=(
                "Read list of paths from standard input and print tree to standard output."
            ),
        )

    def add_arguments(self) -> None:
        """Add arguments to parser."""

        if not PathtreeCLI.prefix or len(PathtreeCLI.prefix) == 0:
            title_prefix = ""
            dest_prefix = ""
            prefix = "--"
        else:
            title_prefix = PathtreeCLI.prefix + " "
            dest_prefix = PathtreeCLI.prefix + "_"
            prefix = "--" + PathtreeCLI.prefix + "-"

        group = self.parser.add_argument_group(title_prefix + "formatting options")
        #
        arg = group.add_argument(
            prefix + "style",
            default="round",
            choices=["ascii", "double", "round", "square"],
            help="choose rendering style",
        )
        self.add_default_to_help(arg)

        arg = group.add_argument(
            prefix + "indent",
            default=0,
            type=int,
            metavar="INDENT",
            help="indent output with INDENT spaces",
        )
        self.add_default_to_help(arg)

        arg = group.add_argument(
            prefix + "lengthen",
            default=0,
            type=int,
            metavar="COLUMNS",
            help="lengthen horizontal lines by COLUMNS",
        )
        self.add_default_to_help(arg)

        #
        dirname_short = group.add_mutually_exclusive_group()
        dest = dest_prefix + "dirname_short"

        arg = dirname_short.add_argument(
            prefix + "dirname-short",
            action="store_true",
            dest=dest,
            help="with short dirnames",
        )
        self.add_default_to_help(arg)

        arg = dirname_short.add_argument(
            prefix + "dirname-long",
            action="store_false",
            dest=dest,
            help="with long dirnames",
        )
        self.add_default_to_help(arg)

        arg = dirname_short.add_argument(
            prefix + "dirname-wrap",
            default=66,
            type=int,
            metavar="COLUMN",
            help="wrap dirnames at COLUMN",
        )
        self.add_default_to_help(arg)

        #
        basename_short = group.add_mutually_exclusive_group()
        dest = dest_prefix + "basename_short"

        arg = basename_short.add_argument(
            prefix + "basename-short",
            action="store_true",
            dest=dest,
            help="with short basenames",
        )
        self.add_default_to_help(arg)

        arg = basename_short.add_argument(
            prefix + "basename-long",
            action="store_false",
            dest=dest,
            help="with long basenames",
        )
        self.add_default_to_help(arg)

        arg = basename_short.add_argument(
            prefix + "basename-wrap",
            default=66,
            type=int,
            metavar="COLUMN",
            help="wrap basenames at COLUMN",
        )
        self.add_default_to_help(arg)

        arg = self.parser.add_argument(
            "FILE",
            nargs="?",
            type=argparse.FileType(),
            default=sys.stdin,
            help="read paths from `FILE` instead of `stdin`",
        )

    def main(self) -> None:
        """Command line interface entry point (method)."""

        tree = PathTree()
        for line in self.options.FILE:
            tree.addpath(line.strip())

        for art, text, _ in tree.render(
            style=self.options.style,
            indent=self.options.indent,
            lengthen=self.options.lengthen,
            dirname_short=self.options.dirname_short,
            dirname_wrap=self.options.dirname_wrap,
            basename_short=self.options.basename_short,
            basename_wrap=self.options.basename_wrap,
        ):
            print(art + text)


def main(args: list[str] | None = None) -> None:
    """Command line interface entry point (function)."""
    PathtreeCLI(args).main()
