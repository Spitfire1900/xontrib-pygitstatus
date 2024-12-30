# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# # pylint: disable=redefined-outer-name
import contextlib
import os
from collections import abc
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest
from git import Remote, RemoteReference, Repo
from xonsh.built_ins import XonshSession
from xonsh.prompt.base import PromptFields, PromptFormatter
from xonsh.xontribs import xontribs_loaded

if TYPE_CHECKING:
    from xonsh.environ import Env

# test_gitstatus: https://github.com/xonsh/xonsh/blob/0.12.5/tests/prompt/test_gitstatus.py#L65


@pytest.fixture
def git_repo(tmp_path):
    repo = Repo.init(tmp_path)
    assert isinstance(tmp_path, PathLike)
    yield repo


@contextlib.contextmanager
def cd(path: PathLike):
    resource = Path(path)
    old_dir = Path.cwd()
    try:
        os.chdir(resource)
        yield
    finally:
        os.chdir(old_dir)


@pytest.fixture(scope="function", autouse=True)
def prompts(load_xontrib: abc.Callable[[str], None],
            xonsh_session: XonshSession) -> abc.Generator[PromptFields, Any, Any]:
    load_xontrib('pygitstatus')
    assert 'pygitstatus' in xontribs_loaded()
    xonsh_env: Env = xonsh_session.env  # type: ignore reportAssignmentType
    prompts: PromptFields = xonsh_env.get(
        'PROMPT_FIELDS')  # type: ignore reportAssignmentType
    assert 'pygitstatus' in prompts
    yield prompts


def test_ahead(git_repo, tmp_path):
    with cd(git_repo.working_tree_dir):
        remote: Remote = git_repo.create_remote('origin', tmp_path)
        remote.fetch()
        git_repo.index.commit('initial commit')
        remote_ref = RemoteReference(
            git_repo, f'refs/remotes/origin/{git_repo.active_branch.name}')
        git_repo.active_branch.set_tracking_branch(remote_ref)
        remote.push()
        git_repo.index.commit('commit 2')
        assert PromptFormatter()('{pygitstatus.ahead}') == '↑·1'


def test_behind(git_repo, tmp_path):
    with cd(git_repo.working_tree_dir):
        remote: Remote = git_repo.create_remote('origin', tmp_path)
        remote.fetch()
        init_commit = git_repo.index.commit('initial commit')
        git_repo.index.commit('commit 2')
        remote_ref = RemoteReference(
            git_repo, f'refs/remotes/origin/{git_repo.active_branch.name}')
        git_repo.active_branch.set_tracking_branch(remote_ref)
        remote.push()
        git_repo.active_branch.set_commit(init_commit)
        assert PromptFormatter()('{pygitstatus.behind}') == '↓·1'


def test_branch(git_repo):
    with cd(git_repo.working_tree_dir):
        git_repo.index.commit('initial commit')
        git_repo.create_head('test_branch')
        git_repo.git.checkout('test_branch')
        assert PromptFormatter()('{pygitstatus.branch}') == '{CYAN}test_branch'


# HACK this can not run at the same time as other branch_bg_color tests
@pytest.mark.forked
def test_branch_bg_color_red(git_repo):
    with cd(git_repo.working_tree_dir):
        Path('empty_file.txt').touch()
        assert PromptFormatter()('{pygitstatus.branch_bg_color}') == '{BACKGROUND_RED}'


# HACK this can not run at the same time as other branch_bg_color tests
@pytest.mark.forked
def test_branch_bg_color_yellow(tmp_path):
    with cd(tmp_path):
        assert PromptFormatter()(
            '{pygitstatus.branch_bg_color}') == '{BACKGROUND_YELLOW}'


# HACK this can not run at the same time as other branch_bg_color tests
@pytest.mark.forked
def test_branch_bg_color_green(git_repo):
    with cd(git_repo.working_tree_dir):
        assert PromptFormatter()(
            '{pygitstatus.branch_bg_color}') == '{BACKGROUND_GREEN}'


# HACK this can not run at the same time as other branch_branch_color tests
@pytest.mark.forked
def test_branch_color_red(git_repo):
    with cd(git_repo.working_tree_dir):
        Path('empty_file.txt').touch()
        assert PromptFormatter()('{pygitstatus.branch_color}') == '{BOLD_INTENSE_RED}'


# HACK this can not run at the same time as other branch_branch_color tests
@pytest.mark.forked
def test_branch_color_yellow(tmp_path):
    with cd(tmp_path):
        assert PromptFormatter()(
            '{pygitstatus.branch_color}') == '{BOLD_INTENSE_YELLOW}'


# HACK this can not run at the same time as other branch_branch_color tests
@pytest.mark.forked
def test_branch_color_green(git_repo):
    with cd(git_repo.working_tree_dir):
        assert PromptFormatter()('{pygitstatus.branch_color}') == '{BOLD_INTENSE_GREEN}'


def test_changed(git_repo):
    with cd(git_repo.working_tree_dir):
        # XXX: Testing initial state prevents final state check from working
        # assert PromptFormatter()('{pygitstatus.changed}') == ''
        workfile = Path('workfile.txt')
        workfile.touch()
        git_repo.git.add(workfile)
        git_repo.index.commit('initial commit')
        workfile.write_text('Hello world!', encoding='utf-8')
        assert PromptFormatter()('{pygitstatus.changed}') == '{BLUE}+1{RESET}'


def test_clean(git_repo):
    with cd(git_repo.working_tree_dir):
        assert PromptFormatter()('{pygitstatus.clean}') == '{BOLD_GREEN}✓{RESET}'


def test_curr_branch(git_repo):
    with cd(git_repo.working_tree_dir):
        # an initial commit is required
        git_repo.index.commit('initial commit')
        assert PromptFormatter()(
            '{pygitstatus_curr_branch}') == f'{git_repo.active_branch.name}'


def test_deleted(git_repo):
    with cd(git_repo.working_tree_dir):
        workfile = Path('workfile.txt')
        workfile.touch()
        git_repo.git.add(workfile)
        git_repo.index.commit('initial commit')
        workfile.unlink()
        assert PromptFormatter()('{pygitstatus.deleted}') == '{RED}-1{RESET}'


def test_lines_added(git_repo):
    with cd(git_repo.working_tree_dir):
        workfile = Path('workfile.txt')
        workfile.touch()
        git_repo.git.add(workfile)
        git_repo.index.commit('initial commit')
        lines = 3
        workfile.write_text(os.linesep.join({str(i)
                                             for i in range(1, lines + 1)}),
                            encoding='utf-8')
        assert PromptFormatter()(
            '{pygitstatus.lines_added}') == f'{{CYAN}}+{lines}{{RESET}}'


def test_lines_deleted(git_repo):
    with cd(git_repo.working_tree_dir):
        workfile = Path('workfile.txt')
        lines = 3
        workfile.write_text(os.linesep.join({str(i)
                                             for i in range(1, lines + 1)}),
                            encoding='utf-8')
        git_repo.git.add(workfile)
        git_repo.index.commit('initial commit')
        workfile.write_text('', encoding='utf-8')
        assert PromptFormatter()(
            '{pygitstatus.lines_deleted}') == f'{{INTENSE_RED}}-{lines}{{RESET}}'


def test_numstat(git_repo):
    with cd(git_repo.working_tree_dir):
        insertions_workfile = Path('insertions.txt')
        deletions_workfile = Path('deletions.txt')
        insertions = 2
        deletions = 3

        insertions_workfile.touch()
        deletions_workfile.write_text(
            os.linesep.join({str(i)
                             for i in range(1, deletions + 1)}), encoding='utf-8')

        git_repo.git.add(insertions_workfile, deletions_workfile)
        git_repo.index.commit('initial commit')

        insertions_workfile.write_text(
            os.linesep.join({str(i)
                             for i in range(1, insertions + 1)}), encoding='utf-8')
        deletions_workfile.write_text('', encoding='utf-8')

        assert PromptFormatter()(
            '{pygitstatus.numstat}') == f'({insertions}, {deletions})'


def test_repo_path(git_repo):
    with cd(git_repo.working_tree_dir):
        assert PromptFormatter()('{pygitstatus.repo_path}') == '.git'


def test_short_head(git_repo):
    with cd(git_repo.working_tree_dir):
        git_repo.index.commit('initial commit')
        # The OOTB default for git is 7,
        # but this _could_ be affected by a user's core.abbrev setting
        short_head = git_repo.commit().name_rev[:7]
        assert PromptFormatter()('{pygitstatus.short_head}') == f':{short_head}'


def test_untracked(git_repo):
    with cd(git_repo.working_tree_dir):
        Path('text.txt').touch()
        assert PromptFormatter()('{pygitstatus.untracked}') == '…1'
