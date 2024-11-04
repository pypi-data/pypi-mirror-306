"""Process front matter."""

from markdown_it import MarkdownIt


def front_matter_plugin(md: MarkdownIt) -> None:
    """Plugin ported from
    `markdown-it-front-matter <https://github.com/ParkSB/markdown-it-front-matter>`__.

    It parses initial metadata, stored between opening/closing dashes:

    .. code-block:: md

        ---
        valid-front-matter: true
        ---

    """
    from .worker import _front_matter_rule

    md.block.ruler.before(
        "table",
        "front_matter",
        _front_matter_rule,
        {"alt": ["paragraph", "reference", "blockquote", "list"]},
    )
