import contextlib
import os

from pygit2 import (
    Commit,
    Diff,
    GitError,
)
from pygit2.enums import (
    DescribeStrategy,
    FileStatus,
)
from pygit2.repository import Repository as Repo
from xonsh.prompt.base import (
    MultiPromptField,
    PromptField,
    PromptFields,
)
from xonsh.prompt.gitstatus import operations as gitstatus_operations

# pylint: disable=no-name-in-module

### .venv/Lib/site-packages/xonsh/prompt/gitstatus.py


@PromptField.wrap(prefix='↑·', info='ahead', name='pygitstatus.ahead')
def ahead(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    _ahead, _behind = (0, 0)
    with contextlib.suppress(GitError):
        repo = Repo('.')

        local_commit = repo.head.target
        local_branch = repo.branches.get(repo.head.shorthand)
        if local_branch is not None and (upstream := local_branch.upstream) is not None:
            upstream_commit = upstream.target
            _ahead, _behind = repo.ahead_behind(local_commit, upstream_commit)

    fld.value = str(_ahead) if _ahead else ''


@PromptField.wrap(prefix='↓·', info='behind', name='pygitstatus.behind')
def behind(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    _ahead, _behind = (0, 0)
    with contextlib.suppress(GitError):
        repo = Repo('.')

        local_commit = repo.head.target
        local_branch = repo.branches.get(repo.head.shorthand)
        if local_branch is not None and (upstream := local_branch.upstream) is not None:
            upstream_commit = upstream.target
            _ahead, _behind = repo.ahead_behind(local_commit, upstream_commit)

    fld.value = str(_behind) if _behind else ''


@PromptField.wrap(prefix='{CYAN}', info='branch', name='pygitstatus.branch')
def branch(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')
        fld.value = repo.head.shorthand


def branch_bg_color() -> str:
    color = '{BACKGROUND_YELLOW}'
    with contextlib.suppress(GitError):
        repo = Repo('.')
        color = '{BACKGROUND_GREEN}' if len(repo.status()) == 0 else '{BACKGROUND_RED}'
    return color


def branch_color() -> str:
    color = '{BOLD_INTENSE_YELLOW}'
    with contextlib.suppress(GitError):
        repo = Repo('.')
        color = '{BOLD_INTENSE_GREEN}' if len(
            repo.status()) == 0 else '{BOLD_INTENSE_RED}'
    return color


@PromptField.wrap(prefix="{BLUE}+", suffix="{RESET}", info="changed",
                  name='pygitstatus.changed')
def changed(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    count = 0

    with contextlib.suppress(GitError):
        repo = Repo('.')

        for file_status in repo.status().values():
            if FileStatus.WT_MODIFIED & file_status:
                count = count + 1
        if count > 0:
            fld.value = str(count)


@PromptField.wrap(
    prefix="{RED}×",  # noqa: RUF001
    suffix="{RESET}",
    info="conflicts",
    name='pygitstatus.conflicts',
)
def conflicts(fld: PromptField, ctx: PromptFields):
    # NOTE: gitstatus does not include conflicted files when both are added
    #       to the index and the working tree
    #       pygitstatus will though
    #       This is an intentional difference
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')
        conflicted_count = len([
            file_status for file_status in repo.status().values()
            if FileStatus.CONFLICTED & file_status
        ])
        if conflicted_count > 0:
            fld.value = str(conflicted_count)


@PromptField.wrap(prefix='{BOLD_GREEN}', suffix='{RESET}', symbol='✓',
                  name='pygitstatus.clean')
def clean(fld: PromptField, ctx: PromptFields):

    # symbol attribute is auto-populated by wrap function
    symbol: str
    symbol = fld.symbol  # type: ignore

    fld.value = ''

    with contextlib.suppress(GitError):
        repo = Repo('.')
        if len(repo.status()) == 0:
            fld.value = symbol


def curr_branch() -> str | None:
    with contextlib.suppress(GitError):
        repo = Repo('.')
        return repo.head.shorthand


@PromptField.wrap(prefix="{RED}-", suffix="{RESET}", info="deleted",
                  name='pygitstatus.deleted')
def deleted(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    count = 0

    with contextlib.suppress(GitError):
        repo = Repo('.')

        for file_status in repo.status().values():
            if FileStatus.WT_DELETED & file_status:
                count = count + 1
        if count > 0:
            fld.value = str(count)


@PromptField.wrap(prefix="{CYAN}+", suffix="{RESET}", name='pygitstatus.lines_added')
def lines_added(fld: PromptField, ctx: PromptFields):
    fld.value = ''

    with contextlib.suppress(GitError):
        repo = Repo('.')
        diff = repo.diff()
        if isinstance(diff, Diff) and (inserts := diff.stats.insertions) > 0:
            fld.value = str(inserts)


@PromptField.wrap(prefix="{INTENSE_RED}-", suffix="{RESET}",
                  name='pygitstatus.lines_deleted')
def lines_deleted(fld: PromptField, ctx: PromptFields):
    fld.value = ''

    with contextlib.suppress(GitError):
        repo = Repo('.')
        diff = repo.diff()
        if isinstance(diff, Diff) and (deletes := diff.stats.deletions) > 0:
            fld.value = str(deletes)


@PromptField.wrap(name='pygitstatus.numstat')
def numstat(fld: PromptField, ctx: PromptFields):
    fld.value = str((0, 0))
    insert = 0
    delete = 0

    with contextlib.suppress(GitError):
        repo = Repo('.')
        diff = repo.diff()
        if isinstance(diff, Diff):
            insert = diff.stats.insertions
            delete = diff.stats.deletions
    fld.value = str((insert, delete))


operations = gitstatus_operations


@PromptField.wrap(name='pygitstatus.repo_path')
def repo_path(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')

        # this returns `.git` in most cases, should it
        # just return the relative basedir?
        fld.value = os.path.relpath(repo.path)


@PromptField.wrap(prefix=':', name='pygitstatus.short_head')
def short_head(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')
        local_commit_hash = repo.head.target
        if (local_commit := repo.get(local_commit_hash)) is not None:
            fld.value = local_commit.short_id


@PromptField.wrap(prefix="{RED}●", suffix="{RESET}", info="staged",
                  name='pygitstatus.staged')
def staged(fld: PromptField, ctx: PromptFields):
    # NOTE: Conflict files are intentionally excluded from the staged count.
    #       This is an intentional difference from gitstatus.
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')
        untracked_count = len([
            file_status for file_status in repo.status().values() if any([
                FileStatus.INDEX_MODIFIED & file_status,
                FileStatus.INDEX_NEW & file_status,
                FileStatus.INDEX_RENAMED & file_status,
                FileStatus.INDEX_TYPECHANGE & file_status,
                # Conflicts are intentionally excluded, unlike gitstatus
                # FileStatus.CONFLICTED & file_status,
            ])
        ])
        if untracked_count > 0:
            fld.value = str(untracked_count)


@PromptField.wrap(prefix="⚑", name='pygitstatus.stash_count')
def stash_count(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')
        _stash_count = len(repo.listall_stashes())
        if _stash_count > 0:
            fld.value = str(_stash_count)


@PromptField.wrap(name='pygitstatus.tag')
def tag(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')
        fld.value = repo.describe(describe_strategy=DescribeStrategy.TAGS)


@PromptField.wrap(name='pygitstatus.tag_or_hash')
def tag_or_hash(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')
        fld.value = repo.describe(describe_strategy=DescribeStrategy.TAGS)

    if not fld.value:
        with contextlib.suppress(GitError):
            repo = Repo('.')
            fld.value = repo.lookup_reference(repo.head.name).peel(
                Commit).short_id  #type: ignore # pylance can't tell that this is fine


@PromptField.wrap(prefix="…", info="untracked", name='pygitstatus.untracked')
def untracked(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')
        untracked_count = len([
            file_status for file_status in repo.status().values()
            if FileStatus.WT_NEW & file_status
        ])
        if untracked_count > 0:
            fld.value = str(untracked_count)


class PyGitStatus(MultiPromptField):
    """Return str `BRANCH|OPERATOR|numbers`"""

    # NOTE: gitstatus does not include conflicted files when both are added
    #       to the index and the working tree
    # assert PromptFormatter()('{pygitstatus}') == PromptFormatter()('{gitstatus}')
    # This comes from git status --porcelain
    # @ git status --porcelain
    # AM changed_file.txt
    # AA conflict_file.txt
    # AD deleted.txt
    # ?? untracked.txt
    # ----
    # Since conflict_file.txt is added in both the index and the working tree,
    # pygitstatus intentionally differs from gitstatus in this case
    # pygitstatus also intentionally excludes conflicted files from the staged count

    _name = 'pygitstatus'
    fragments = (
        ".branch",
        ".ahead",
        ".behind",
        ".operations",
        "{RESET}|",
        ".staged",
        ".conflicts",
        ".changed",
        ".deleted",
        ".untracked",
        ".stash_count",
        ".lines_added",
        ".lines_removed",
        ".clean",
    )
    hidden = (
        ".lines_added",
        ".lines_removed",
    )
    """These fields will not be processed for the result"""

    def get_frags(self, env):
        for frag in self.fragments:
            if frag in self.hidden:
                continue
            yield frag


pygitstatus = PyGitStatus()
