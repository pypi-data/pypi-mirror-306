import hashlib
import os
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

StrPath = os.PathLike[str] | str
_T = TypeVar('_T')


class Algorithm(ABC, Generic[_T]):
    """
    Base class for algorithms.
    """

    def __init__(
        self, width: int, height: int, fill: _T, digest: bytes | None = None
    ) -> None:
        """
        Initializes an algorithm.

        Args:
            width: Matrix width.
            height: Matrix height.
            fill: Default matrix value.
            digest: Input bytes.
        """
        self._matrix = [[fill for _ in range(width)] for _ in range(height)]
        self._x = width // 2
        self._y = height // 2
        if digest is not None:
            self.update(digest)

    @abstractmethod
    def update(self, data: bytes) -> None:
        """
        Feeds bytes into the algorithm.

        Args:
            data: Input bytes.
        """
        pass

    def update_from_path(
        self, path: StrPath, hash_function: str = 'sha256'
    ) -> None:
        """
        Feeds a file digest into the algorithm.

        Args:
            path: File path.
            hash_function: Hash function.
        """
        with open(path, 'rb') as f:
            digest = hashlib.file_digest(f, hash_function).digest()
            self.update(digest)

    def __getitem__(self, key: tuple[int, int]) -> _T:
        x, y = key
        return self._matrix[y][x]

    def __setitem__(self, key: tuple[int, int], value: _T) -> None:
        x, y = key
        self._matrix[y][x] = value

    @property
    def width(self) -> int:
        """
        Matrix width.
        """
        if not self._matrix:
            return 0
        return len(self._matrix[0])

    @property
    def height(self) -> int:
        """
        Matrix height.
        """
        return len(self._matrix)

    def overlay(
        self,
        matrix: list[list[_T]],
        x_off: int,
        y_off: int,
        ignore: _T | None = None,
    ) -> 'Algorithm[_T]':
        """
        Overlays a matrix over this one.

        Args:
            other: Matrix to overlay.
            x_off: X-axis offset.
            y_off: Y-axis offset.
            ignore: Value to ignore while overlaying.

        Returns:
            Self.
        """
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val == ignore:
                    continue
                new_y = y + y_off
                new_x = x + x_off
                if 0 <= new_y < self.height and 0 <= new_x < self.width:
                    self[new_x, new_y] = val
        return self

    def to_art(
        self,
        framed: bool = True,
        top_text: str | None = None,
        bottom_text: str | None = None,
        brackets: tuple[str, str] = ('[', ']'),
        lines: tuple[str, str, str, str] = ('-', '|', '-', '|'),
        corners: tuple[str, str, str, str] = ('+', '+', '+', '+'),
    ) -> str:
        """
        Generates randomart.

        Args:
            framed: Whether randomart should be framed.
            top_text: Text on the top line.
            bottom_text: Text on the bottom line.
            brackets: Symbols surrounding text.
            lines: Frame side symbols in a clockwise order from the top.
            corners: Frame corner symbols in a clockwise order from the top-left.

        Returns:
            Randomart.
        """  # noqa: E501
        art = self._to_art()

        if not framed:
            return art

        art_lines = art.split('\n')
        width = len(art_lines[0])

        # unpacking the values from tuples
        frame_t, frame_r, frame_b, frame_l = lines
        corner_tl, corner_tr, corner_br, corner_bl = corners

        br_len = len(brackets[0]) + len(brackets[1])
        if top_text is None:
            top_text = ''
        else:
            top_len = len(top_text) + br_len
            if top_len > width:
                top_text = top_text[: width - top_len - 3] + '...'
            top_text = top_text.join(brackets)

        if bottom_text is None:
            bottom_text = ''
        else:
            bot_len = len(bottom_text) + br_len
            if bot_len > width:
                bottom_text = bottom_text[: width - bot_len - 3] + '...'
            bottom_text = bottom_text.join(brackets)

        top_line = top_text.center(width, frame_t).join((corner_tl, corner_tr))
        bot_line = bottom_text.center(width, frame_b).join(
            (corner_bl, corner_br)
        )
        content = '\n'.join(f'{frame_l}{line}{frame_r}' for line in art_lines)
        art = '\n'.join((top_line, content, bot_line))
        return art

    @abstractmethod
    def _to_art(self) -> str:
        pass
