### pathtree - An os.PathLike wrapper around anytree.RenderTree

#### Usage
    pathtree [--style {ascii,double,round,square}] [--indent INDENT]
             [--lengthen COLUMNS]
             [--dirname-short | --dirname-long | --dirname-wrap COLUMN]
             [--basename-short | --basename-long | --basename-wrap COLUMN]
             [-h] [-v] [-V] [--print-config] [--print-url]
             [--completion [SHELL]]
             [FILE]
    
Read list of paths from standard input and print tree to standard output.

#### Positional Arguments
    FILE                Read paths from `FILE` instead of `stdin`.

#### formatting options
    --style {ascii,double,round,square}
                        Choose rendering style (default: `round`).
    --indent INDENT     Indent output with INDENT spaces (default: `0`).
    --lengthen COLUMNS  Lengthen horizontal lines by COLUMNS (default: `0`).
    --dirname-short     With short dirnames (default: `False`).
    --dirname-long      With long dirnames (default: `True`).
    --dirname-wrap COLUMN
                        Wrap dirnames at COLUMN (default: `66`).
    --basename-short    With short basenames (default: `False`).
    --basename-long     With long basenames (default: `True`).
    --basename-wrap COLUMN
                        Wrap basenames at COLUMN (default: `66`).

#### General options
    -h, --help          Show this help message and exit.
    -v, --verbose       `-v` for detailed output and `-vv` for more detailed.
    -V, --version       Print version number and exit.
    --print-config      Print effective config and exit.
    --print-url         Print project url and exit.
    --completion [SHELL]
                        Print completion scripts for `SHELL` and exit
                        (default: `bash`).
