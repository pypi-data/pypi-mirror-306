"""Command line interface."""

from pathlib import Path

import xdg
from libcli import BaseCLI
from loguru import logger
from pathtree.cli import PathtreeCLI

from sumdups import Sumdups
from sumdups.subfile import File

__all__ = ["SumdupsCLI"]


class SumdupsCLI(BaseCLI):
    """Command line interface."""

    config = {
        # distribution name, not importable package name
        "dist-name": "rlane-sumdups",
    }

    def init_parser(self) -> None:
        """Initialize argument parser."""

        self.parser = self.ArgumentParser(
            prog=__package__,
            description="Find duplicate files based on checksum (hash or digest) of contents.",
        )

    def add_arguments(self) -> None:
        """Add arguments to parser."""

        self.parser.add_argument(
            "-q", "--quiet", action="store_true", help="suppress no-action warnings"
        )

        self.parser.add_argument(
            "-n", "--no-action", action="store_true", help="don't change anything"
        )

        self.parser.add_argument(
            "--force", action="store_true", help="always perform expensive calculations"
        )

        #
        database = self.parser.add_mutually_exclusive_group()

        database.add_argument(
            "--database",
            type=Path,
            default=Path(xdg.xdg_cache_home(), __package__, self.parser.prog + ".db"),
            help="use DATABASE",
        )

        database.add_argument(
            "--no-database",
            dest="database",
            default=False,
            action="store_const",
            const=None,
            help="do not use database",
        )

        #
        archive = self.parser.add_mutually_exclusive_group()

        archive.add_argument(
            "--archive",
            type=Path,
            default=Path(xdg.xdg_data_home(), __package__),
            help="create archives in directory ARCDIR",
        )

        archive.add_argument(
            "--no-archive",
            dest="archive",
            default=False,
            action="store_const",
            const=None,
            help="do not archive during rename or remove",
        )

        self.parser.add_argument(
            "--print-extensions",
            action="store_true",
            help="print extensions sorted by occurences",
        )

        self.parser.add_argument(
            "--print-mimetypes", action="store_true", help="print mimetypes sorted by occurences"
        )

        self.parser.add_argument(
            "--print-merged",
            action="store_true",
            help="print merged extensions and mimetypes sorted by occurences",
        )

        self.parser.add_argument(
            "--print-singletons", action="store_true", help="print all singleton files"
        )

        self.parser.add_argument(
            "--print-duplicates", action="store_true", help="print all duplicate files"
        )

        self.parser.add_argument(
            "--print-unique",
            action="store_true",
            help="print one (and only one) pathname for each unique HASH",
        )

        self.parser.add_argument(
            "--suggest", action="store_true", help="print suggested pathnames"
        )

        self.parser.add_argument("--short", action="store_true", help="print pathnames only")

        self.parser.add_argument(
            "--split", action="store_true", help="print with split dirname and basename"
        )

        self.parser.add_argument(
            "--rename",
            metavar="HASH",
            help="rename dupset HASH using the suggested name. "
            "Use `@file` to read list of HASH from file. "
            "Use --local-root DIR to change the suggested root.",
        )

        self.parser.add_argument(
            "--remove",
            metavar="HASH",
            help="remove all files in dupset HASH. "
            "Use `@file` to read list of HASH from file.",
        )

        self.parser.add_argument(
            "--relocate",
            metavar="FILE",
            help="move FILE into the suggested directory. "
            "Use `@file` to read list of FILE from file",
        )

        self.parser.add_argument(
            "--clean-files",
            metavar="DIR",
            help="remove any file in DIR that is part of a dupset",
        )

        self.parser.add_argument(
            "--clean-dir", metavar="DIR", help="remove any file in DIR that is part of a dupset"
        )

        self.parser.add_argument("--keep", metavar="FILE", help="remove all duplicates of FILE")

        self.parser.add_argument(
            "--check-dates",
            action="store_true",
            help="check exif date against suggested directory",
        )

        self.parser.add_argument(
            "--sync", metavar="FILE", help="compare database with list of remote FILEs"
        )

        self.parser.add_argument(
            "--link-farm", metavar="DIR", help="create link-farm at DIR to all src_paths"
        )

        self.parser.add_argument(
            "--print-link-tree", action="store_true", help="print link-tree"
        )

        self.parser.add_argument("--print-folders", action="store_true", help="print folders")

        self.parser.add_argument("--print-files", action="store_true", help="print files")

        self.parser.add_argument(
            "--local-root", metavar="DIR", help="path to the root of the local tree"
        )

        self.parser.add_argument(
            "--remote-root", metavar="DIR", help="path to the root of the remote tree"
        )

        PathtreeCLI.prefix = "pathtree"
        PathtreeCLI.add_arguments(self)

        #
        tree = self.parser.add_argument_group("more tree formatting options")

        tree.add_argument(
            "--width-left", default=87, type=int, metavar="WIDTH", help="width of left column "
        )

        tree.add_argument(
            "--width-center",
            default=16,
            type=int,
            metavar="WIDTH",
            help="width of center column ",
        )

        tree.add_argument(
            "--width-right", default=7, type=int, metavar="WIDTH", help="width of right column "
        )

        #
        colorize = tree.add_mutually_exclusive_group()
        dest = "colorize"

        colorize.add_argument("--color", action="store_true", dest=dest, help="with color")

        colorize.add_argument(
            "--no-color", action="store_false", dest=dest, help="without color"
        )

        # -------------------------------------------------------------------------------

        self.parser.add_argument(
            "src_path", nargs="*", help="source files/directories to search recursively"
        )

    # -------------------------------------------------------------------------------

    def main(self) -> None:
        """Command line interface entry point (method)."""

        # pylint: disable=too-many-branches
        # pylint: disable=too-many-return-statements
        # pylint: disable=too-many-statements

        sumdups = Sumdups()
        sumdups.options = self.options

        if (  # pylint: disable=too-many-boolean-expressions
            self.options.rename
            or self.options.remove
            or self.options.relocate
            or self.options.clean_files
            or self.options.clean_dir
            or self.options.keep
        ):
            self.options.short = True

        if self.options.local_root:
            File.suggested_root = self.options.local_root

        File.NO_ACTION = self.options.no_action

        #
        sumdups.read_files()
        sumdups.read_database()
        sumdups.load_stats()
        duplicates = sumdups.find_duplicates()
        singletons = sumdups.find_singletons(duplicates)

        total = len(sumdups.Files_by_pathname)
        assert total == sum([len(_) for _ in duplicates.values()])  # noqa
        ndups = total - len(singletons)

        logger.debug(
            "files {} singletons {} duplicates {} unique-cksums {}",
            total,
            len(singletons),
            ndups,
            len(duplicates),
        )

        # -------------------------------------------------------------------------------
        # work things; do the work, and leave the database alone

        if self.options.rename:
            sumdups.rename_dupsets(duplicates)
            return

        if self.options.remove:
            sumdups.remove_dupsets(duplicates)
            return

        if self.options.relocate:
            sumdups.relocate_files(duplicates)
            return

        if self.options.clean_files:
            sumdups.clean_files(duplicates)
            return

        if self.options.clean_dir:
            sumdups.clean_dir(duplicates)
            return

        if self.options.keep:
            sumdups.keep(duplicates)
            return

        if self.options.check_dates:
            sumdups.check_dates()
            return

        if self.options.sync:
            sumdups.sync()
            return

        if self.options.link_farm:
            sumdups.link_farm()
            return

        # -------------------------------------------------------------------------------
        # print things

        if self.options.print_singletons:
            sumdups.print_singletons(duplicates, singletons)

        if self.options.print_duplicates:
            sumdups.print_duplicates(duplicates)

        if self.options.print_unique:
            sumdups.print_unique()

        if self.options.print_link_tree:
            sumdups.print_link_tree()

        if self.options.print_folders:
            sumdups.print_folders()

        if self.options.print_files:
            sumdups.print_files()

        if self.options.print_extensions:
            sumdups.print_extensions()

        if self.options.print_mimetypes:
            sumdups.print_mimetypes()

        if self.options.print_merged:
            sumdups.print_merged()

        #
        sumdups.write_database()


def main(args: list[str] | None = None) -> None:
    """Command line interface entry point (function)."""
    SumdupsCLI(args).main()
