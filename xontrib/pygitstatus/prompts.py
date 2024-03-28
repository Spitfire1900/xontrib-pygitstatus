import contextlib
import os
from typing import Optional

# pylint: disable=no-name-in-module
from pygit2 import (GIT_STATUS_CONFLICTED, GIT_STATUS_INDEX_MODIFIED,
                    GIT_STATUS_INDEX_NEW, GIT_STATUS_INDEX_RENAMED,
                    GIT_STATUS_INDEX_TYPECHANGE, GIT_STATUS_WT_DELETED,
                    GIT_STATUS_WT_MODIFIED, GIT_STATUS_WT_NEW, Commit, Diff, GitError)
from pygit2 import Repository as Repo
from xonsh.prompt.base import MultiPromptField, PromptField, PromptFields

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


@PromptField.wrap(prefix="{BLUE}+", suffix="{RESET}", info="changed",
                  name='pygitstatus.changed')
def changed(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')
        untracked_count = len(
            [v for k, v in repo.status().items() if v == GIT_STATUS_WT_MODIFIED])
        if untracked_count > 0:
            fld.value = str(untracked_count)


@PromptField.wrap(prefix="{RED}×", suffix="{RESET}", info="conflicts",
                  name='pygitstatus.conflicts')
def conflicts(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')
        conflicted_count = len(
            [v for k, v in repo.status().items() if v == GIT_STATUS_CONFLICTED])
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


def curr_branch() -> Optional[str]:
    with contextlib.suppress(GitError):
        repo = Repo('.')
        return repo.head.shorthand


@PromptField.wrap(prefix="{RED}-", suffix="{RESET}", info="deleted",
                  name='pygitstatus.deleted')
def deleted(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')
        untracked_count = len(
            [v for k, v in repo.status().items() if v == GIT_STATUS_WT_DELETED])
        if untracked_count > 0:
            fld.value = str(untracked_count)


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
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')
        untracked_count = len([
            v for k, v in repo.status().items() if v in [
                GIT_STATUS_INDEX_MODIFIED,
                GIT_STATUS_INDEX_NEW,
                GIT_STATUS_INDEX_RENAMED,
                GIT_STATUS_INDEX_TYPECHANGE,
            ]
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
        fld.value = repo.describe()


@PromptField.wrap(name='pygitstatus.tag_or_hash')
def tag_or_hash(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')
        fld.value = repo.describe()

    if not fld.value:
        with contextlib.suppress(GitError):
            repo = Repo('.')
            fld.value = repo.lookup_reference(repo.head.name).peel(Commit).short_id


@PromptField.wrap(prefix="…", info="untracked", name='pygitstatus.untracked')
def untracked(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')
        untracked_count = len(
            [v for k, v in repo.status().items() if v == GIT_STATUS_WT_NEW])
        if untracked_count > 0:
            fld.value = str(untracked_count)


class GitStatus(MultiPromptField):
    """Return str `BRANCH|OPERATOR|numbers`"""

    _name = 'pygitstatus'
    fragments = (
        ".branch",
        ".ahead",
        ".behind",
        "gitstatus.operations",  # does not use subprocess calls
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


gitstatus = GitStatus()
