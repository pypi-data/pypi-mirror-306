### sumdups - checksum/duplicates, yada...

#### Usage
    sumdups [-q] [-n] [--force] [--database DATABASE | --no-database]
            [--archive ARCHIVE | --no-archive] [--print-extensions]
            [--print-mimetypes] [--print-merged] [--print-singletons]
            [--print-duplicates] [--print-unique] [--suggest] [--short]
            [--split] [--rename HASH] [--remove HASH] [--relocate FILE]
            [--clean-files DIR] [--clean-dir DIR] [--keep FILE]
            [--check-dates] [--sync FILE] [--link-farm DIR]
            [--print-link-tree] [--print-folders] [--print-files]
            [--local-root DIR] [--remote-root DIR]
            [--pathtree-style {ascii,double,round,square}]
            [--pathtree-indent INDENT] [--pathtree-lengthen COLUMNS]
            [--pathtree-dirname-short | --pathtree-dirname-long | --pathtree-dirname-wrap COLUMN]
            [--pathtree-basename-short | --pathtree-basename-long | --pathtree-basename-wrap COLUMN]
            [--width-left WIDTH] [--width-center WIDTH]
            [--width-right WIDTH] [--color | --no-color] [-h] [-v] [-V]
            [--print-config] [--print-url] [--completion [SHELL]]
            [FILE] [src_path ...]
    
Find duplicate files based on checksum (hash or digest) of contents.

#### Positional Arguments
    FILE                Read paths from `FILE` instead of `stdin`.
    src_path            Source files/directories to search recursively.

#### Options
    -q, --quiet         Suppress no-action warnings.
    -n, --no-action     Don't change anything.
    --force             Always perform expensive calculations.
    --database DATABASE
                        Use DATABASE.
    --no-database       Do not use database.
    --archive ARCHIVE   Create archives in directory ARCDIR.
    --no-archive        Do not archive during rename or remove.
    --print-extensions  Print extensions sorted by occurences.
    --print-mimetypes   Print mimetypes sorted by occurences.
    --print-merged      Print merged extensions and mimetypes sorted by
                        occurences.
    --print-singletons  Print all singleton files.
    --print-duplicates  Print all duplicate files.
    --print-unique      Print one (and only one) pathname for each unique
                        HASH.
    --suggest           Print suggested pathnames.
    --short             Print pathnames only.
    --split             Print with split dirname and basename.
    --rename HASH       Rename dupset HASH using the suggested name. Use
                        `@file` to read list of HASH from file. Use --local-
                        root DIR to change the suggested root.
    --remove HASH       Remove all files in dupset HASH. Use `@file` to read
                        list of HASH from file.
    --relocate FILE     Move FILE into the suggested directory. Use `@file` to
                        read list of FILE from file.
    --clean-files DIR   Remove any file in DIR that is part of a dupset.
    --clean-dir DIR     Remove any file in DIR that is part of a dupset.
    --keep FILE         Remove all duplicates of FILE.
    --check-dates       Check exif date against suggested directory.
    --sync FILE         Compare database with list of remote FILEs.
    --link-farm DIR     Create link-farm at DIR to all src_paths.
    --print-link-tree   Print link-tree.
    --print-folders     Print folders.
    --print-files       Print files.
    --local-root DIR    Path to the root of the local tree.
    --remote-root DIR   Path to the root of the remote tree.

#### pathtree formatting options
    --pathtree-style {ascii,double,round,square}
                        Choose rendering style (default: `round`).
    --pathtree-indent INDENT
                        Indent output with INDENT spaces (default: `0`).
    --pathtree-lengthen COLUMNS
                        Lengthen horizontal lines by COLUMNS (default: `0`).
    --pathtree-dirname-short
                        With short dirnames (default: `False`).
    --pathtree-dirname-long
                        With long dirnames (default: `True`).
    --pathtree-dirname-wrap COLUMN
                        Wrap dirnames at COLUMN (default: `66`).
    --pathtree-basename-short
                        With short basenames (default: `False`).
    --pathtree-basename-long
                        With long basenames (default: `True`).
    --pathtree-basename-wrap COLUMN
                        Wrap basenames at COLUMN (default: `66`).

#### more tree formatting options
    --width-left WIDTH  Width of left column .
    --width-center WIDTH
                        Width of center column .
    --width-right WIDTH
                        Width of right column .
    --color             With color.
    --no-color          Without color.

#### General options
    -h, --help          Show this help message and exit.
    -v, --verbose       `-v` for detailed output and `-vv` for more detailed.
    -V, --version       Print version number and exit.
    --print-config      Print effective config and exit.
    --print-url         Print project url and exit.
    --completion [SHELL]
                        Print completion scripts for `SHELL` and exit
                        (default: `bash`).
