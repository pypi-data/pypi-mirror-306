"""Extend `libfile.File`."""

# -------------------------------------------------------------------------------

import hashlib
import os
import time
from datetime import datetime
from pathlib import Path

import libfile
import magic
from dateutil.parser import parse as parse_date
from loguru import logger

# -------------------------------------------------------------------------------


class File(libfile.File):
    """Docstring."""

    # pylint: disable=too-many-instance-attributes

    suggested_root = Path.home()
    _suggested_name = None

    def __init__(self, *args, **kwargs):
        """Docstring."""

        super().__init__(*args, **kwargs)

        self.cksum = None
        self.mimetype = None
        self.exif_datetime = None
        self.prev_mtime = None
        self.prev_size = None
        self.is_cmdline_arg = False

        # meaningful only when self.isdir
        self.num_files_children = 0
        self.total_bytes_children = 0

    # -------------------------------------------------------------------------------

    def load_stats(self, args, et):
        """Docstring."""

        if (
            not args.force
            and self.exists
            and self.prev_mtime == int(self.stats.st_mtime)
            and self.prev_size == self.stats.st_size
        ):
            logger.trace("Unchanged {!r}", self.pathname)

        elif not self.exists:
            logger.info("Gone {!r}", self.pathname)

        else:
            if not self.cksum:
                logger.info("New file {!r}", self.pathname)
            else:
                logger.info("Changed {!r}", self.pathname)

            self.load_cksum()
            self.load_mimetype()
            self.load_exifdate(et)

    # -------------------------------------------------------------------------------

    def load_cksum(self):
        """Docstring."""

        # print(hashlib.algorithms_available)

        with open(self.pathname, "rb") as f:
            checksum = hashlib.sha1()
            for chunk in iter(lambda: f.read(65536), b""):
                checksum.update(chunk)

        self.cksum = checksum.hexdigest()

        logger.debug("{!r} {!r}", self.pathname, self.cksum)

    # -------------------------------------------------------------------------------

    def load_mimetype(self):
        """Docstring."""

        self.mimetype = magic.from_file(self.pathname, mime=True)

        logger.debug("{!r} {!r}", self.pathname, self.mimetype)

    # -------------------------------------------------------------------------------

    def load_exifdate(self, et):
        """Docstring."""

        # pylint: disable=too-many-branches

        metadata = et.get_metadata(self.pathname)

        for k, v in metadata.items():
            if "date" in k.lower():
                logger.trace("{:30} {}", k, v)

        tags = (
            "EXIF:DateTimeOriginal",
            "EXIF:CreateDate",  # noqa:
            "QuickTime:CreateDate",  # noqa:
            "PDF:CreateDate",  # noqa:
            "XML:CreateDate",  # noqa:
            "CreateDate",  # noqa:
            "CreatedDate",  # noqa:
            "CreationDate",  # noqa:
            "EXIF:ModifyDate",  # noqa:
            "QuickTime:ModifyDate",  # noqa:
            "PDF:ModifyDate",  # noqa:
            "XML:ModifyDate",  # noqa:
            "ModifyDate",  # noqa:
        )

        dates = {k: v for (k, v) in metadata.items() if k in tags}

        if not dates:
            return

        dates = sorted(dates.items(), key=lambda _: _[1])
        # logger.debug('{!r} dates {!r}', self.pathname, dates)

        tag = dates[0][0]
        value = dates[0][1].strip()
        # logger.debug('{!r} oldest {!r} {!r}', self.pathname, tag, value)

        if not value:
            return

        if value.startswith("0000"):
            return

        # Parse the date into a long.
        #
        # Some are like this: "2017:07:14 16:19:34"
        # Some are like this: "2017/07/14 16:19:34"
        # Some PDF like this: "D:20080708224141Z"
        # Some PDF like this: "D:20150108114410-05'00'"
        # Some JPG like this: "Thu Aug 05 16:25:07 2010"
        # Some JPG like this: '2011:05:15 22:30: 9'

        fmt = None
        n = len(value)

        if value[2].isdigit():
            if value.startswith("D:"):
                fmt = "D:%Y%m%d%H%M%S"
                if value[-1] == "Z":
                    value = value[:-1]
                elif value.endswith("'00'"):
                    value = value[:-4] + "00"
                    fmt += "%z"
            elif n >= 19:  # len('YYYY.mm.dd HH.MM.SS')
                if value[4] == ":":
                    fmt = "%Y:%m:%d %H:%M:%S"
                elif value[4] == "/":
                    fmt = "%Y/%m/%d %H:%M:%S"
                if value[17] == " ":
                    value = value[:17] + "0" + value[18:]
                if fmt and n > 19:
                    fmt += "%z"

        try:
            if fmt:
                dt = datetime.strptime(value, fmt)
            else:
                dt = parse_date(value)
        except Exception as e:  # noqa: broad-exception-caught
            logger.error("{!r} Can't parse {!r}: {}", self.pathname, value, e)
            return

        self.exif_datetime = int(dt.timestamp())

        logger.debug("{!r} {!r} {!r}", self.pathname, tag, self.format_ts(self.exif_datetime))

    # -------------------------------------------------------------------------------

    @staticmethod
    def format_ts(timestamp):
        """Docstring."""

        if not timestamp:
            return "-"
        return time.strftime("%F %T", time.localtime(timestamp))

    # -------------------------------------------------------------------------------

    @staticmethod
    def format_pathname(args, pathname):
        """Docstring."""

        if not args.split:
            return f"{pathname!r}"

        return "{os.path.dirname(pathname)!r:62} {os.path.basename(pathname)!r}"

    # -------------------------------------------------------------------------------

    @property
    def suggested_name(self):
        """Docstring."""

        if self._suggested_name is None:

            if "image" in self.mimetype or "video" in self.mimetype:
                folder = "Pictures"
            elif "audio" in self.mimetype:
                folder = "Music"
            else:
                folder = "Documents"

            _ = time.localtime(self.exif_datetime or int(self.stats.st_mtime))
            subfolder, basename = time.strftime("%Y-%m %Y%m%d-%H%M%S", _).split()

            _, ext = os.path.splitext(self.pathname)

            self._suggested_name = (
                os.path.join(self.suggested_root, folder, subfolder, basename) + ext
            )

        return self._suggested_name


# -------------------------------------------------------------------------------
