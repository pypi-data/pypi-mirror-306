import argparse
import base64
import hashlib
from io import BufferedReader, TextIOWrapper
from pathlib import Path
from typing import Sequence

from hashime.__version__ import __version__
from hashime.algorithm import Algorithm
from hashime.drunken_bishop import DrunkenBishop

_algorithms: list[type[Algorithm]] = [DrunkenBishop]


def cli(argv: Sequence[str] | None = None):
    algorithms = {algorithm.__name__: algorithm for algorithm in _algorithms}
    parser = argparse.ArgumentParser(
        prog='hashime',
        description='hash visualization tool',
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=__version__,
    )

    parser.add_argument(
        '-l',
        '--list',
        nargs=0,
        action=PrintAndExitAction,
        const=f"""\
Algorithms:\n    {', '.join(algorithms.keys())}
Hash Functions:\n    {', '.join(sorted(hashlib.algorithms_available))}""",
        help='show visualization algorithms and hashing functions and exit',
    )

    parser.add_argument(
        '-a',
        '--algorithm',
        choices=algorithms.keys(),
        default='DrunkenBishop',
        metavar='ALGO',
        help='visualization algorithm (defaults to DrunkenBishop)',
    )

    parser.add_argument(
        '-H',
        '--hash-function',
        choices=hashlib.algorithms_available,
        default='sha256',
        metavar='HASH',
        help='hashing function (defaults to sha256)',
    )

    parser.add_argument(
        '--width',
        type=int,
        help='visualization width',
    )

    parser.add_argument(
        '--height',
        type=int,
        help='visualization height',
    )

    parser.add_argument(
        '--no-frame',
        action='store_true',
        help='output visualization without a frame',
    )

    parser.add_argument(
        '--frame-top-text',
        metavar='TOP_TEXT',
        help='text on the top frame line',
    )

    parser.add_argument(
        '--frame-bottom-text',
        metavar='BOTTOM_TEXT',
        help='text on the bottom frame line',
    )

    parser.add_argument(
        '--frame-lines',
        metavar='LINES',
        help='comma-separated frame side symbols '
        'in a clockwise order from the top',
    )

    parser.add_argument(
        '--frame-corners',
        metavar='CORNERS',
        help='comma-separated frame corner symbols '
        'in a clockwise order from the top-left',
    )

    parser.add_argument(
        '--frame-brackets',
        metavar='BRACKETS',
        help='comma-separated symbols surrounding frame text',
    )

    parser.add_argument(
        '-d',
        '--digest',
        action='store_true',
        help='output digest',
    )

    parser.add_argument(
        '-f',
        '--file',
        type=argparse.FileType('br'),
        default='-',
        help='input file (defaults to stdin)',
    )

    parser.add_argument(
        '-o',
        '--output',
        type=argparse.FileType('w'),
        default='-',
        metavar='OUT',
        help='output file (defaults to stdout)',
    )

    args = parser.parse_args(argv)

    algorithm = algorithms[args.algorithm]
    hash_function: str = args.hash_function
    should_be_framed: bool = not args.no_frame
    should_show_digest: bool = args.digest
    out: TextIOWrapper = args.output
    file: BufferedReader = args.file

    digest = hashlib.file_digest(file, hash_function).digest()

    algo_kwargs = {}
    if args.width is not None:
        algo_kwargs['width'] = args.width
    if args.height is not None:
        algo_kwargs['height'] = args.height

    frame_kwargs = {}
    if args.frame_lines is not None:
        lines = args.frame_lines.split(',')
        frame_kwargs['lines'] = lines
        if len(lines) != 4:
            raise ValueError(f'Number of line chars is not 4: {len(lines)}')
    if args.frame_corners is not None:
        corners = args.frame_corners.split(',')
        frame_kwargs['corners'] = corners
        if len(corners) != 4:
            raise ValueError(
                f'Number of corner chars is not 4: {len(corners)}'
            )
    if args.frame_brackets is not None:
        brackets = args.frame_brackets.split(',')
        frame_kwargs['brackets'] = brackets
        if len(brackets) != 2:
            raise ValueError(
                f'Number of bracket chars is not 2: {len(brackets)}'
            )

    top_text = args.frame_top_text
    bottom_text = args.frame_bottom_text

    if top_text is None:
        top_text = Path(file.name).name
    if bottom_text is None:
        bottom_text = hash_function.upper()

    algo = algorithm(digest=digest, **algo_kwargs)
    art = algo.to_art(
        should_be_framed,
        top_text=top_text or None,
        bottom_text=bottom_text or None,
        **frame_kwargs,
    )

    out.write(art)
    out.write('\n')
    if should_show_digest:
        encoded = base64.standard_b64encode(digest).decode()
        out.write(f'{hash_function}: {encoded}\n')


class PrintAndExitAction(argparse.Action):
    def __call__(self, parser, *_):
        print(self.const)
        parser.exit()


if __name__ == '__main__':
    cli()
