"""An `os.PathLike` wrapper around `anytree.RenderTree`."""

import os
import textwrap
from pathlib import Path

import anytree


class PathTree:
    """An `os.PathLike` wrapper around `anytree.RenderTree`."""

    def __init__(self):
        """Create and return a new PathTree(object)."""

        self.rel_tree = None
        self.abs_tree = None
        self.tree = None

    def addpath(self, path):
        """Graft each node in path onto the tree.

        Unless it's already there, which is ok, like `mkdir -p`.

        Arguments:
            path:       can either be a string representing a pathname,
                        or an object implementing the os.PathLike interface
                        which returns a string, or another path object.
                        See https://docs.python.org/3/library/pathlib.html#pure-paths

        Returns:
            The anytree.Node(object) within self.tree for the given path, where:

            node.name       type(str) form of path.

            node._path      `path` as given; avoiding namespace collision with
                            `anytree.Node.path`.

        """

        # peek inside for string name
        if isinstance(path, Path):
            pathname = str(path)
        elif hasattr(path, "path") and isinstance(path.path, Path):
            pathname = str(path.path)
        else:
            pathname = str(path)
        # now treat it as opaque

        # already exist?
        if node := self.find(pathname):
            return node

        # no, create new node.
        node = anytree.Node(pathname, _path=path)

        if pathname == os.path.sep and not self.abs_tree:
            # just created "/".
            self.abs_tree = node
            return node

        # determine its parent
        parent = None
        dirname = os.path.dirname(str(path))

        if dirname:
            if dirname != os.path.sep and (parent := self.find(dirname)):
                pass
            else:
                parent = self.addpath(dirname)
        else:
            if not self.rel_tree:
                self.rel_tree = anytree.Node("<ROOT>")
            parent = self.rel_tree

        assert parent
        node.parent = parent
        return node

    def find(self, path):
        """Search for `path` in the tree.

        Arguments:
            path:       can either be a string representing a pathname,
                        or an object implementing the os.PathLike interface
                        which returns a string, or another path object.
                        See https://docs.python.org/3/library/pathlib.html#pure-paths

        Returns:        the Node found or None.
        """

        if isinstance(path, Path):
            pathname = str(path)
        elif hasattr(path, "path") and isinstance(path.path, Path):
            pathname = str(path.path)
        else:
            pathname = str(path)

        node = None
        if self.abs_tree:
            node = anytree.search.find(self.abs_tree, lambda node: node.name == pathname)

        if not node and self.rel_tree:
            node = anytree.search.find(self.rel_tree, lambda node: node.name == pathname)

        return node

    def render(
        self,
        *,
        style="round",
        indent=0,
        lengthen=0,
        dirname_short=True,
        dirname_wrap=0,
        basename_short=True,
        basename_wrap=0,
    ):
        """Docstring."""

        # pylint: disable=too-many-arguments

        for self.tree in (self.abs_tree, self.rel_tree):  # noqa: B020 Found for loop that...
            yield from self._render(
                style=style,
                indent=indent,
                lengthen=lengthen,
                dirname_short=dirname_short,
                dirname_wrap=dirname_wrap,
                basename_short=basename_short,
                basename_wrap=basename_wrap,
            )

    def _render(
        self,
        *,
        style="round",
        indent=0,
        lengthen=0,
        dirname_short=True,
        dirname_wrap=0,
        basename_short=True,
        basename_wrap=0,
    ):

        # pylint: disable=too-many-arguments
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-locals

        if not self.tree:
            return

        if isinstance(style, str):
            if style == "ascii":
                style = anytree.AsciiStyle()
            elif style in ("DoubleStyle", "double"):
                style = anytree.DoubleStyle()
            elif style in ("ContRoundStyle", "round"):
                style = anytree.ContRoundStyle()
            elif style in ("ContRoundStyle", "square"):
                style = anytree.ContStyle()
            else:
                raise ValueError(f"invalid style {style!r}")

        indent = " " * indent if indent else ""

        if lengthen:
            style.vertical = self._lengthen(style.vertical, lengthen)
            style.cont = self._lengthen(style.cont, lengthen)
            style.end = self._lengthen(style.end, lengthen)

        #
        flag = False
        for pre, fill, node in anytree.RenderTree(self.tree, style=style):
            if node.name == "<ROOT>":
                flag = True
                continue
            if flag:
                pre = pre[4:]
                if fill:
                    fill = fill[4:]

            short = basename_short if node.is_leaf else dirname_short
            wrap = basename_wrap if node.is_leaf else dirname_wrap

            name = os.path.basename(node.name) if short else node.name

            # pylint: disable=protected-access
            if not wrap:
                yield indent + pre, name, node._path
            else:
                lines = textwrap.wrap(name, width=wrap)
                yield indent + pre, lines.pop(0), node._path
                for line in lines:
                    yield indent + fill, line, None

    @staticmethod
    def _lengthen(text, length):
        if not text or len(text) < 2:
            return text
        return text[:-2] + (text[-2] * length) + text[-2:]

    def print(self, *args, **kwargs):
        """Docstring."""

        for art, text, path in self.render(*args, **kwargs):
            print(art, text, path)
