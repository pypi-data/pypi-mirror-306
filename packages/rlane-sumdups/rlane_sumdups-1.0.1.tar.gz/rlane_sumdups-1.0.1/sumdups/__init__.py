"""Find duplicate files based on checksum (hash or digest) of contents."""

# -------------------------------------------------------------------------------

import json
import os
import tempfile
import time
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile

import exiftool
from loguru import logger
from pathtree.pathtree import PathTree
from termcolor import colored

from sumdups.subfile import File

# -------------------------------------------------------------------------------


class Sumdups:
    """Docstring."""

    # pylint: disable=too-many-public-methods

    Files_by_pathname = {}  # Key=pathname, Value=File
    fill = unicodedata.lookup("ONE DOT LEADER")
    options = None
    # fill = unicodedata.lookup('BOX DRAWINGS LIGHT HORIZONTAL')

    # -------------------------------------------------------------------------------

    def archive(self, basename, files):
        """Docstring."""

        if not self.options.archive:
            if not self.options.quiet:
                logger.opt(depth=1).warning("Not archiving")
            return

        zipname = os.path.join(self.options.archive, basename + ".zip")

        if self.options.no_action:
            if not self.options.quiet:
                logger.opt(depth=1).warning("Not creating {!r}", zipname)
            return

        logger.opt(depth=1).info("Creating {!r}", zipname)

        with ZipFile(zipname, "w") as zipper:
            for file in files:
                logger.opt(depth=1).debug("Adding {!r}", file.pathname)
                zipper.write(file.pathname)

    # -------------------------------------------------------------------------------

    def read_files(self):
        """Get current state, from filesystem."""

        for file in File.walk(self.options.src_path):
            file.is_cmdline_arg = True
            self.Files_by_pathname[file.pathname] = file

    # -------------------------------------------------------------------------------

    def read_database(self):
        """Get previous state, from database."""

        if not self.options.database:
            if not self.options.quiet:
                logger.warning("Not using database")
            return

        if not self.options.database.exists():
            if not self.options.quiet:
                logger.warning("Can't find database {!r}", str(self.options.database))
            return

        logger.info("Reading database {!r}", str(self.options.database))

        with self.options.database.open() as db:
            for line in db:
                cksum, size, mtime, mimetype, exif_datetime, pathname = line.strip().split(
                    maxsplit=5
                )

                file = self.Files_by_pathname.get(pathname)
                if not file:
                    file = File(pathname)
                    if not file.exists:
                        logger.info("Gone {!r}", file.pathname)
                        continue
                    self.Files_by_pathname[pathname] = file

                file.cksum = cksum
                file.mimetype = mimetype
                file.exif_datetime = int(exif_datetime)
                file.prev_mtime = int(mtime)
                file.prev_size = int(size)

    # -------------------------------------------------------------------------------

    def write_database(self):
        """Docstring."""

        # pylint: disable=too-many-branches

        # assert not args.rename and not args.relocate  # why?
        assert not self.options.rename
        assert not self.options.relocate

        if not self.options.database:
            if not self.options.quiet:
                logger.warning("Not using database")
            return

        if self.options.no_action:
            if not self.options.quiet:
                logger.warning("Not writing database {!r}", str(self.options.database))
            return

        # Write new database to tmpfile in same location

        self.options.database.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w+t",
            prefix="sumdups",
            suffix=".tmpdb",
            dir=self.options.database.parent,
            delete=False,
        ) as tmpfile:

            logger.info("Writing database {!r}", tmpfile.name)

            for pathname, file in sorted(self.Files_by_pathname.items()):
                if not file.exists:
                    logger.trace("Gone {!r}", file.pathname)
                    continue
                tmpfile.write(
                    " ".join(
                        [
                            str(file.cksum),
                            str(file.stats.st_size),
                            str(int(file.stats.st_mtime)),
                            file.mimetype,
                            str(file.exif_datetime) if file.exif_datetime else "0",
                            pathname,
                        ]
                    )
                    + "\n"
                )

        newfile = File(tmpfile.name)

        # Backup and install new database, if changed

        if not self.options.database.exists():
            logger.debug("No database to backup {!r}", str(self.options.database))
        else:
            newfile.load_cksum()
            oldfile = File(self.options.database)
            oldfile.load_cksum()

            if newfile.cksum == oldfile.cksum:
                logger.info("Database unchanged")
                os.unlink(newfile.pathname)
                return

            # Backup the old database
            ts = time.strftime(
                "-%Y%m%d-%H%M%S", time.localtime(self.options.database.stat().st_mtime)
            )
            backup = Path(str(self.options.database) + ts)
            assert not backup.exists()

            if self.options.no_action:
                if not self.options.quiet:
                    logger.warning(
                        "Not backing up {!r} -> {!r}", str(self.options.database), str(backup)
                    )
            else:
                logger.info("Backing up {!r} -> {!r}", str(self.options.database), str(backup))
                self.options.database.rename(backup)

        # Install the new database

        if self.options.no_action:
            if not self.options.quiet:
                logger.warning("Not installing new database {!r}", str(self.options.database))
            os.unlink(newfile.pathname)
        else:
            logger.info("Installing new database {!r}", str(self.options.database))
            os.rename(newfile.pathname, self.options.database)

    # -------------------------------------------------------------------------------

    def load_stats(self):
        """Docstring."""

        with exiftool.ExifTool() as et:
            for file in self.Files_by_pathname.values():
                file.load_stats(et)

    # -------------------------------------------------------------------------------

    def find_duplicates(self):
        """Docstring."""

        file_lists_by_cksum = defaultdict(list)  # Key=cksum, Value=list(File)
        for file in self.Files_by_pathname.values():
            file_lists_by_cksum[file.cksum].append(file)

        return file_lists_by_cksum

    # -------------------------------------------------------------------------------

    @staticmethod
    def find_singletons(file_lists_by_cksum):
        """Docstring."""

        singletons = []

        for files in file_lists_by_cksum.values():
            if len(files) == 1:
                singletons.append(files[0])

        return singletons

    # -------------------------------------------------------------------------------
    # Printing methods
    # -------------------------------------------------------------------------------

    def print_singletons(self, file_lists_by_cksum, singletons):
        """Docstring."""

        if not self.options.short:
            print("===== SINGLETONS ".ljust(120, "="))

        for file in sorted(singletons, key=lambda _: _.pathname):
            if self.options.short:
                print(file.pathname)
            else:
                self.print_dupset(file.cksum, file_lists_by_cksum[file.cksum])

    # -------------------------------------------------------------------------------

    def print_duplicates(self, file_lists_by_cksum):
        """Docstring."""

        if not self.options.short:
            print("===== DUPLICATES ".ljust(120, "="))

        cksums = Counter()
        for file in self.Files_by_pathname.values():
            cksums[file.cksum] += 1

        for cksum, nfiles in sorted(cksums.items(), key=lambda _: _[1], reverse=True):
            if nfiles < 2:
                break
            files = file_lists_by_cksum[cksum]
            if not self.options.src_path or any([_.is_cmdline_arg for _ in files]):  # noqa
                self.print_dupset(cksum, files)

    # -------------------------------------------------------------------------------

    def print_unique(self):
        """Docstring."""

        for file in self._unique():
            print(file.pathname)

    # -------------------------------------------------------------------------------

    def _unique(self):

        filtering = {}
        for file in File.walk(self.options.src_path):
            filtering[str(file.path.absolute())] = True

        seen = {}
        for pathname, file in sorted(self.Files_by_pathname.items()):
            if (not filtering or filtering.get(pathname)) and not seen.get(file.cksum):
                seen[file.cksum] = True
                yield file

    # -------------------------------------------------------------------------------

    def print_dupset(self, cksum, files):
        """Docstring."""

        file = files[0]

        print(f"--- {len(files)} {cksum} {file.mimetype}".ljust(120, "-"))

        for file in sorted(files, key=lambda _: _.pathname):

            if not file.exif_datetime:
                delta = "-"
            else:
                delta = int(file.stats.st_mtime) - file.exif_datetime

            print(
                str.format(
                    "DUP: {:10} {:19} {:19} {:9} {}",
                    file.stats.st_size,
                    file.format_ts(int(file.stats.st_mtime)),
                    file.format_ts(file.exif_datetime),
                    delta,
                    file.format_pathname(file.pathname),
                )
            )

        if self.options.suggest:
            print(f"SUGGEST: {'':56} {file.format_pathname(file.suggested_name)}")

    # -------------------------------------------------------------------------------

    def print_extensions(self):
        """Docstring."""

        counter = Counter()
        for pathname in self.Files_by_pathname:
            _, ext = os.path.splitext(pathname)
            counter[ext.lower()] += 1

        for key, count in sorted(counter.items(), key=lambda _: _[1], reverse=True):
            print(f"{count:5} {key!r}")

    # -------------------------------------------------------------------------------

    def print_mimetypes(self):
        """Docstring."""

        counter = Counter()
        for file in self.Files_by_pathname.values():
            counter[file.mimetype] += 1

        for key, count in sorted(counter.items(), key=lambda _: _[1], reverse=True):
            print(f"{count:5} {key!r}")

    # -------------------------------------------------------------------------------

    def print_merged(self):
        """Docstring."""

        counter = Counter()
        for file in self.Files_by_pathname.values():
            _, ext = os.path.splitext(file.pathname)
            counter[ext.lower()] += 1
            counter[file.mimetype] += 1

        for key, count in sorted(counter.items(), key=lambda _: _[1], reverse=True):
            print(f"{count:5} {key!r}")

    # -------------------------------------------------------------------------------
    # Action methods
    # -------------------------------------------------------------------------------

    def _rename_files(self, cksum, files, target=None):

        assert len(files)

        self.print_dupset(cksum, files)
        self.archive(cksum, files)

        file = files[0]  # any one will do
        if not target:
            target = File(file.suggested_name)

        if target not in files:
            if not target.mkparent():
                return
            file.rename(target)

        for file in files:
            if file == target:
                logger.opt(depth=1).info("Retaining {!r}", file.pathname)
            else:
                file.unlink()

    # -------------------------------------------------------------------------------

    def rename_dupsets(self, file_lists_by_cksum):
        """Docstring."""

        assert self.options.rename

        for cksum in File.expand_atfiles(self.options.rename):

            files = file_lists_by_cksum.get(cksum)
            if not files:
                logger.error("Can't find cksum {!r}", cksum)

            elif len(files) < 2:
                logger.warning("Not a dupset {!r}", cksum)

            else:
                self._rename_files(cksum, files)

    # -------------------------------------------------------------------------------

    def remove_dupsets(self, file_lists_by_cksum):
        """Docstring."""

        assert self.options.remove

        for cksum in File.expand_atfiles(self.options.remove):

            files = file_lists_by_cksum.get(cksum)
            if not files:
                logger.error("Can't find cksum {!r}", cksum)

            else:
                self._remove_files(cksum, files)

    # -------------------------------------------------------------------------------

    def _remove_files(self, cksum, files):

        assert len(files)

        self.print_dupset(cksum, files)
        self.archive(cksum, files)

        for file in files:
            file.unlink()

    # -------------------------------------------------------------------------------

    def relocate_files(self, file_lists_by_cksum):
        """Relocate files into the suggested directory, keeping the original basenames."""

        assert self.options.relocate

        for pathname in File.expand_atfiles(self.options.relocate):

            file = self.Files_by_pathname.get(pathname)
            if not file or not file.exists:
                logger.error("Can't find {!r}", pathname)
                continue

            target = File(
                os.path.join(
                    os.path.dirname(file.suggested_name),
                    os.path.basename(file.pathname),
                )
            )

            self._rename_files(file.cksum, file_lists_by_cksum[file.cksum], target)

    # -------------------------------------------------------------------------------

    def clean_files(self, file_lists_by_cksum):
        """Docstring."""

        assert self.options.clean

        for pathname in File.expand_atfiles(self.options.clean):

            file = self.Files_by_pathname.get(pathname)
            if not file:
                logger.error("Not in database {!r}", pathname)
                continue

            files = file_lists_by_cksum[file.cksum]
            if len(files) < 2:
                logger.info("Not a duplicate {!r}", pathname)
                continue

            self.print_dupset(file.cksum, files)
            file.unlink()

    # -------------------------------------------------------------------------------

    def clean_dir(self, file_lists_by_cksum):
        """Docstring."""

        assert self.options.clean_dir
        len_clean_dir = len(self.options.clean_dir)

        for file in self.Files_by_pathname.values():

            logger.error(file)

            if file.pathname[:len_clean_dir] != self.options.clean_dir:
                logger.debug(
                    "{!r} != {!r}", self.options.clean_dir, file.pathname[:len_clean_dir]
                )
                continue

            files = file_lists_by_cksum[file.cksum]
            if len(files) < 2:
                logger.warning("Not a duplicate {!r}", file.pathname)
                continue

            has_dup_outside_dir = False
            for dup in [_ for _ in files if _ != file]:
                if dup.pathname[:len_clean_dir] != self.options.clean_dir:
                    logger.info("file {!r} outside dup {!r}", file.pathname, dup.pathname)
                    has_dup_outside_dir = True
                    break

            if not has_dup_outside_dir:
                logger.debug("not has_dup_outside_dir {}", has_dup_outside_dir)
                continue

            logger.debug("has_dup_outside_dir {}", has_dup_outside_dir)
            for dup in files:
                if dup.pathname[:len_clean_dir] == self.options.clean_dir and dup.exists:
                    dup.unlink()

    # -------------------------------------------------------------------------------

    def keep(self, file_lists_by_cksum):
        """Docstring."""

        assert self.options.keep

        for pathname in File.expand_atfiles(self.options.keep):

            file = self.Files_by_pathname.get(pathname)
            if not file:
                logger.error("Not in database {!r}", pathname)
                continue

            files = file_lists_by_cksum[file.cksum]
            if len(files) < 2:
                logger.info("Not a duplicate {!r}", pathname)
                continue

            for dup in files:
                if dup == file:
                    logger.info("Keeping {!r}", dup)
                else:
                    dup.unlink()

    # -------------------------------------------------------------------------------

    def check_dates(self):
        """Docstring."""

        for file in self.Files_by_pathname.values():
            if not file.pathname.startswith("/home/rlane/ext/Ginger/Pictures/"):
                continue
            if not file.exif_datetime:
                continue
            # logger.info(file)
            # logger.info('pathname {!r} exif_datetime {!r}', file.pathname, file.exif_datetime)
            # logger.info('pathname {!r}', file.pathname)
            # logger.info('suggestd {!r}', file.suggested_name)

            ahead, atail = os.path.split(file.pathname)
            adir = os.path.basename(ahead)

            bhead, _ = os.path.split(file.suggested_name)
            bdir = os.path.basename(bhead)

            if adir != bdir:
                dst = os.path.join(bhead, atail)
                assert not os.path.exists(dst)
                # logger.error('COLLISION {!r} {!r}', file.pathname, dst)

                logger.info("Suggest mv {!r} {!r}", file.pathname, dst)
                print(json.dumps({"src": file.pathname, "target": dst}))

    # -------------------------------------------------------------------------------

    def sync(self):
        """Docstring."""

        local = self.options.local_root  # '/home/rlane/ext/Ginger/Pictures/'
        locallen = len(local)
        remote = self.options.remote_root  # '/My Drive/Ginger-PC/Pictures/'

        remote_pathnames = {}
        with open(self.options.sync, encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()
                if line:
                    remote_pathnames[line] = True

        for file in self.Files_by_pathname.values():

            if not file.pathname.startswith(local):
                # logger.error('whoa')
                continue

            local_rel_pathname = file.pathname[locallen:]

            remote_abs_pathname = remote + local_rel_pathname

            if remote_pathnames.get(remote_abs_pathname):
                logger.debug("in sync {!r}", remote_abs_pathname)
            else:
                if file.mimetype.startswith("video"):
                    logger.info(
                        "Skipping {!r} {!r} -> {!r}",
                        file.mimetype,
                        file.pathname,
                        remote_abs_pathname,
                    )
                    continue
                logger.info(
                    "Need to upload {!r} {!r} -> {!r}",
                    file.mimetype,
                    file.pathname,
                    remote_abs_pathname,
                )
                print(json.dumps({"src": file.pathname, "target": remote_abs_pathname}))

    # -------------------------------------------------------------------------------

    def link_farm(self):
        """Docstring."""

        for file in self._unique():
            linkpath = os.path.join(self.options.link_farm, file.pathname[1:])
            file.symlink(linkpath, parents=True)

    # -------------------------------------------------------------------------------

    def print_link_tree(self):
        """Docstring."""

        return

    #        # k=year, v=defaultdict(list) of File by cksum
    #        years = defaultdict(lambda : defaultdict(list))
    #
    #        tfiles = tsize = 0
    #        for file in cls._unique(args):
    #            yyyy, mm = os.path.basename(os.path.dirname(file.suggested_name)).split('-')
    #            years[yyyy][mm].append(file)
    #            tfiles += 1
    #            tsize += file.stats.st_size
    #
    #        #
    #        root = 'root'
    #        tree = {root: OrderedDict([])}
    #
    #        for year, months in sorted(years.items()):
    #            tree[root][year] = OrderedDict([])
    #            for month, files in sorted(months.items()):
    #                tree[root][year][month] = {}
    #
    #        treelines = LeftAligned(draw=BoxStyle(gfx=BOX_LIGHT, indent=1))(tree).splitlines()
    #
    #        # root
    #        print_tree_line(treelines.pop(0), tfiles, tsize)
    #
    #        #
    #        for year, months in sorted(years.items()):
    #
    #            yfiles = sum([len(_) for _ in months.values()])
    #            ysize = 0
    #            for files in months.values():
    #                ysize += sum([_.stats.st_size for _ in files])
    #
    #            for month, files in sorted(months.items()):
    #                mfiles = len(files)
    #                msize = sum([_.stats.st_size for _ in files])
    #
    #                print_tree_line(treelines.pop(0), mfiles, msize)

    # -------------------------------------------------------------------------------

    @staticmethod
    def print_tree_line(line, nfiles, size):
        """Docstring."""

        # horz = BOX_LIGHT['HORIZONTAL']
        horz = "\u2504"
        # horz = u'\u2508'

        nfiles = f" {nfiles:,}".rjust(10, horz)
        size = f" {size:,}".rjust(16, horz)
        stats = nfiles + " files " + size + " bytes"

        line += " "
        padding = (65 - (len(line) + len(stats))) * horz
        print(line, padding, stats, sep="")

    # -------------------------------------------------------------------------------

    def print_folders(self):
        """Docstring."""
        return self._print_tree(show_files=False)

    # -------------------------------------------------------------------------------

    def print_files(self):
        """Docstring."""
        return self._print_tree(show_files=True)

    # -------------------------------------------------------------------------------

    def _print_tree(self, show_files):

        # pylint: disable=too-many-branches
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements

        tree = PathTree()
        for file in self.Files_by_pathname.values():
            if not self.options.src_path or file.is_cmdline_arg:

                # add this file's parent to the tree
                # logger.debug('file {!r}', file)
                node = tree.addpath(File(file.path.parent))

                # roll this file's size up into all parents
                while node:
                    # logger.debug('type {!r} node {!r}', type(node), node)
                    # it's not a "name"; it's the thing given to addpath above
                    f = node.name
                    f.num_files_children += 1
                    f.total_bytes_children += file.stats.st_size
                    node = node.parent

                if show_files:
                    tree.addpath(file)

        # tree.print()

        color_art = "yellow"
        color_text = "blue"
        color_attr1 = "green"
        color_attr2 = "red"

        for art, text, file in tree.render(
            style=self.options.pathtree_style,
            indent=self.options.pathtree_indent,
            lengthen=self.options.pathtree_lengthen,
            dirname_short=self.options.pathtree_dirname_short,
            dirname_wrap=self.options.pathtree_dirname_wrap,
            basename_short=self.options.pathtree_basename_short,
            basename_wrap=self.options.pathtree_basename_wrap,
        ):
            len_left = len(art) + len(text)
            if self.options.colorize:
                if art:
                    art = colored(art, color_art)
                if text:
                    text = colored(text, color_text)
            left = art + text

            if not file:
                print(left)
                continue

            left += " "
            len_left += 1
            if (n := self.options.width_left - len_left) > 0:
                trailer = self.fill * n
                if self.options.colorize:
                    trailer = colored(trailer, color_art)
                left += trailer

            if file.isdir:
                attr1 = f" {file.total_bytes_children:,} "
                len_attr1 = len(attr1)
                if self.options.colorize:
                    attr1 = colored(attr1, color_attr1)
                if (n := self.options.width_center - len_attr1) > 0:
                    leader = self.fill * n
                    if self.options.colorize:
                        leader = colored(leader, color_art)
                    attr1 = leader + attr1

                attr2 = f" {file.num_files_children:,}"
                len_attr2 = len(attr2)
                if self.options.colorize:
                    attr2 = colored(attr2, color_attr2)
                if (n := self.options.width_right - len_attr2) > 0:
                    leader = self.fill * n
                    if self.options.colorize:
                        leader = colored(leader, color_art)
                    attr2 = leader + attr2

                # print(left + attr1 + attr2)
                print(left + attr1 + attr2)
            else:
                attr1 = f" {file.stats.st_size:,} "
                len_attr1 = len(attr1)
                if self.options.colorize:
                    attr1 = colored(attr1, color_attr1)
                if (n := self.options.width_center - len_attr1) > 0:
                    leader = self.fill * n
                    if self.options.colorize:
                        leader = colored(leader, color_art)
                    attr1 = leader + attr1
                print(left + attr1)


# -------------------------------------------------------------------------------
