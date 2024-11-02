"""
Hash visualization tool inspired by beautiful ssh-keygen randomart.

Typical usage as CLI::

    $ hashime -f LICENSE
    +----[LICENSE]----+
    |    ..o +        |
    |   o E.= o       |
    |  o +.. o        |
    | . o o.o         |
    |.   o =.S.       |
    |..   o.+..+      |
    |o.  o.oo+..=     |
    |. . *+=..+o o .  |
    |  .=+O.++  . o.. |
    +-----[SHA256]----+

Typical usage in code::

    >>> import hashime
    >>> bishop = hashime.DrunkenBishop()
    >>> bishop.update_from_path('./LICENSE')
    >>> art = bishop.to_art(top_text='LICENSE', bottom_text='SHA256')
    >>> print(art)
    +----[LICENSE]----+
    |    ..o +        |
    |   o E.= o       |
    |  o +.. o        |
    | . o o.o         |
    |.   o =.S.       |
    |..   o.+..+      |
    |o.  o.oo+..=     |
    |. . *+=..+o o .  |
    |  .=+O.++  . o.. |
    +-----[SHA256]----+
"""

from hashime.drunken_bishop import DrunkenBishop

__all__ = ['DrunkenBishop']
