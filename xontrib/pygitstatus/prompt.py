import contextlib
import os

from pygit2 import GitError  # pylint: disable=no-name-in-module
from pygit2 import Repository as Repo
from xonsh.prompt.base import MultiPromptField, PromptField, PromptFields

### .venv/Lib/site-packages/xonsh/prompt/gitstatus.py


@PromptField.wrap(prefix="{BOLD_GREEN}", suffix="{RESET}", symbol="✓")
def clean(fld: PromptField, ctx: PromptFields):

    # symbol attribute is auto-populated by wrap function
    symbol: str
    symbol = fld.symbol  # type: ignore

    value = ''

    with contextlib.suppress(GitError):
        repo = Repo(os.getcwd())
        if len(repo.status()) == 0:
            value = symbol

    fld.value = value
