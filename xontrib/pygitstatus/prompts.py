import contextlib
import os
from typing import List, Optional

import pygit2
from pygit2 import Commit, Diff, GitError
from pygit2 import Repository as Repo
from pygit2.enums import DescribeStrategy, FileStatus
from xonsh.prompt.base import MultiPromptField, PromptField, PromptFields
from xonsh.prompt.gitstatus import operations as gitstatus_operations

# pylint: disable=no-name-in-module

### .venv/Lib/site-packages/xonsh/prompt/gitstatus.py


def __git_status_list(file_status: int) -> List[int]:
    """
    """
    # pylint: disable=pointless-string-statement,line-too-long
    """
    GIT_STATUS_WT_UNREADABLE: 4096
    GIT_STATUS_WT_RENAMED: 2048
    GIT_STATUS_WT_TYPECHANGE: 1024
    GIT_STATUS_WT_DELETED: 512
    GIT_STATUS_WT_MODIFIED: 256
    GIT_STATUS_WT_NEW: 128
    GIT_STATUS_INDEX_TYPECHANGE: 16
    GIT_STATUS_INDEX_RENAMED: 8
    GIT_STATUS_INDEX_DELETED: 4
    GIT_STATUS_INDEX_MODIFIED: 2
    GIT_STATUS_INDEX_NEW: 1

    TODO: Switch to bitwise operations
    IDEA: enum.FLAG may be useful: https://youtu.be/TAMbq0iRUsA?t=249
    @ [print("{:>013b} is the binary representation of {:>2}".format(i,i)) for i in [4096, 2048, 1024, 512, 256, 128, 16, 8, 4, 2, 1]]
        1000000000000 is the binary representation of 4096
        0100000000000 is the binary representation of 2048
        0010000000000 is the binary representation of 1024
        0001000000000 is the binary representation of 512
        0000100000000 is the binary representation of 256
        0000010000000 is the binary representation of 128
        0000000010000 is the binary representation of 16
        0000000001000 is the binary representation of  8
        0000000000100 is the binary representation of  4
        0000000000010 is the binary representation of  2
        0000000000001 is the binary representation of  1
    @ print("{:>013b}".format(258)); print("{:>013b}".format(256))
        0000100000010
        0000100000000
    @ 256 ^ 258
        2
    @ 528 ^ 16 in [4096, 2048, 1024, 512, 256, 128, 16, 8, 4, 2, 1]
        True
        # This has GIT_STATUS_INDEX_TYPECHANGE status
    """

    statuses = []
    _file_status_worker = file_status

    # pylint: disable=no-member
    for status_int in [
            FileStatus.WT_UNREADABLE,  # 4096
            FileStatus.WT_RENAMED,  # 2048
            FileStatus.WT_TYPECHANGE,  # 1024
            FileStatus.WT_DELETED,  # 512
            FileStatus.WT_MODIFIED,  # 256
            FileStatus.WT_NEW,  # 128
            FileStatus.INDEX_TYPECHANGE,  # 16
            FileStatus.INDEX_RENAMED,  # 8
            FileStatus.INDEX_DELETED,  # 4
            FileStatus.INDEX_MODIFIED,  # 2
            FileStatus.INDEX_NEW,  # 1
    ]:
        if _file_status_worker == 0:
            break
        if _file_status_worker - status_int >= 0:
            statuses.append(status_int)
            _file_status_worker = _file_status_worker % status_int
    return statuses


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

        for k, v in repo.status().items():
            statuses = __git_status_list(v)
            # We don't care about the index
            is_true = FileStatus.WT_MODIFIED in statuses
            if is_true:
                count = count + 1
        if count > 0:
            fld.value = str(count)


@PromptField.wrap(prefix="{RED}×", suffix="{RESET}", info="conflicts",
                  name='pygitstatus.conflicts')
def conflicts(fld: PromptField, ctx: PromptFields):
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')
        conflicted_count = len(
            [v for k, v in repo.status().items() if v == FileStatus.CONFLICTED])
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
    count = 0

    with contextlib.suppress(GitError):
        repo = Repo('.')

        for k, v in repo.status().items():
            statuses = __git_status_list(v)
            # We don't care about the index.
            is_true = FileStatus.WT_DELETED in statuses
            if is_true:
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
    fld.value = ''
    with contextlib.suppress(GitError):
        repo = Repo('.')
        untracked_count = len([
            v for k, v in repo.status().items() if v in [
                FileStatus.INDEX_MODIFIED,
                FileStatus.INDEX_NEW,
                FileStatus.INDEX_RENAMED,
                FileStatus.INDEX_TYPECHANGE,
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
        untracked_count = len(
            [v for k, v in repo.status().items() if v == FileStatus.WT_NEW])
        if untracked_count > 0:
            fld.value = str(untracked_count)


class GitStatus(MultiPromptField):
    """Return str `BRANCH|OPERATOR|numbers`"""

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


gitstatus = GitStatus()
