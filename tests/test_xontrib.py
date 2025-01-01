# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# # pylint: disable=redefined-outer-name
import contextlib
import os
from os import PathLike
from pathlib import Path

import pytest
from git import (
    GitCommandError,
    Remote,
    RemoteReference,
    Repo,
)
from xonsh.prompt.base import PromptFormatter

# test_gitstatus: https://github.com/xonsh/xonsh/blob/0.12.5/tests/prompt/test_gitstatus.py#L65


@pytest.fixture(scope="function", autouse=True)
def xsh_with_pygitstatus():
    from xonsh.built_ins import XSH

    XSH.load()
    from xontrib.pygitstatus.entrypoint import _load_xontrib_
    _load_xontrib_(XSH)
    yield XSH
    XSH.unload()
    # NOTE: Testing initial state prevents final state check from evaluating,
    #       so you may only call PromptFormatter() once per test.


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


def test_branch_bg_color_red(git_repo):
    with cd(git_repo.working_tree_dir):
        Path('empty_file.txt').touch()
        assert PromptFormatter()('{pygitstatus.branch_bg_color}') == '{BACKGROUND_RED}'


def test_branch_bg_color_yellow(tmp_path):
    with cd(tmp_path):
        assert PromptFormatter()(
            '{pygitstatus.branch_bg_color}') == '{BACKGROUND_YELLOW}'


def test_branch_bg_color_green(git_repo):
    with cd(git_repo.working_tree_dir):
        print(f'{git_repo.git.status()=}')
        assert PromptFormatter()(
            '{pygitstatus.branch_bg_color}') == '{BACKGROUND_GREEN}'


def test_branch_color_red(git_repo):
    with cd(git_repo.working_tree_dir):
        Path('empty_file.txt').touch()
        assert PromptFormatter()('{pygitstatus.branch_color}') == '{BOLD_INTENSE_RED}'


def test_branch_color_yellow(tmp_path):
    with cd(tmp_path):
        assert PromptFormatter()(
            '{pygitstatus.branch_color}') == '{BOLD_INTENSE_YELLOW}'


def test_branch_color_green(git_repo):
    with cd(git_repo.working_tree_dir):
        assert PromptFormatter()('{pygitstatus.branch_color}') == '{BOLD_INTENSE_GREEN}'


def test_changed(git_repo):
    with cd(git_repo.working_tree_dir):
        workfile = Path('workfile.txt')
        workfile.touch()
        git_repo.git.add(workfile)
        git_repo.index.commit('initial commit')
        workfile.write_text('Hello world!', encoding='utf-8')
        assert PromptFormatter()('{pygitstatus.changed}') == '{BLUE}+1{RESET}'


def test_clean(git_repo):
    with cd(git_repo.working_tree_dir):
        assert PromptFormatter()('{pygitstatus.clean}') == '{BOLD_GREEN}✓{RESET}'


def test_conflict(git_repo):
    with cd(git_repo.working_tree_dir):
        base_commit = git_repo.index.commit('initial commit')
        default_branch = git_repo.active_branch.name
        conflict_file = Path('conflict_file.txt')

        conflict_file.write_text('Hello World!', encoding='utf-8')
        git_repo.git.add(conflict_file)
        git_repo.index.commit('m1')

        git_repo.git.checkout(base_commit)
        git_repo.create_head('f1')
        git_repo.git.checkout('f1')
        conflict_file.write_text('Goodbye World!', encoding='utf-8')
        git_repo.git.add(conflict_file)
        git_repo.index.commit('f1')

        git_repo.git.checkout(default_branch)
        # Should error since there is a conflict
        with contextlib.suppress(GitCommandError):
            git_repo.git.merge('f1')

        assert PromptFormatter()(
            '{pygitstatus.conflicts}') == '{RED}×1{RESET}'  # noqa: RUF001


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


def test_operations(git_repo):
    with cd(git_repo.working_tree_dir):
        base_commit = git_repo.index.commit('initial commit')
        default_branch = git_repo.active_branch.name
        conflict_file = Path('conflict_file.txt')

        conflict_file.write_text('Hello World!', encoding='utf-8')
        git_repo.git.add(conflict_file)
        git_repo.index.commit('m1')

        git_repo.git.checkout(base_commit)
        git_repo.create_head('f1')
        git_repo.git.checkout('f1')
        conflict_file.write_text('Goodbye World!', encoding='utf-8')
        git_repo.git.add(conflict_file)
        git_repo.index.commit('f1')

        git_repo.git.checkout(default_branch)
        # Should error since there is a conflict
        try:
            git_repo.git.merge('f1')
        except GitCommandError as err:
            if 'CONFLICT' not in err.stdout:
                raise err from err

        assert PromptFormatter()('{pygitstatus.operations}') == '{CYAN}|MERGING'


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


def test_staged(git_repo):
    with cd(git_repo.working_tree_dir):
        workfile = Path('workfile.txt')
        workfile.touch()
        git_repo.git.add(workfile)
        assert PromptFormatter()('{pygitstatus.staged}') == '{RED}●1{RESET}'

    # BUG: The following case reports no staged changes
    #     Changes to be committed:
    #         new file:   changed_file.txt
    #         new file:   deleted.txt

    #     Unmerged paths:
    #     (use "git add <file>..." to mark resolution)
    #             both added:      conflict_file.txt


def test_stash_count(git_repo):
    with cd(git_repo.working_tree_dir):
        git_repo.index.commit('initial commit')

        workfile = Path('workfile.txt')
        workfile.touch()
        git_repo.git.stash('--include-untracked')
        # This also works, but because stash() passes args
        # blindly '--include-untracked' is more clear, particularly since
        # '--include-untracked' does not accept arguments so
        # '--include-untracked=true' will throw an error
        # git_repo.git.stash(include_untracked=True)
        assert PromptFormatter()('{pygitstatus.stash_count}') == '⚑1'


def test_tag_annotated(git_repo):
    with cd(git_repo.working_tree_dir):
        git_repo.index.commit('initial commit')
        git_repo.git.tag('v1 -m v1_message'.split(' '))
        assert PromptFormatter()('{pygitstatus.tag}') == 'v1'


def test_tag_unannotated(git_repo):
    with cd(git_repo.working_tree_dir):
        git_repo.index.commit('initial commit')
        git_repo.git.tag('v1')
        assert PromptFormatter()('{pygitstatus.tag}') == 'v1'


def test_tag_or_hash_annotated(git_repo):
    with cd(git_repo.working_tree_dir):
        git_repo.index.commit('initial commit')
        git_repo.git.tag('v1 -m v1_message'.split(' '))
        assert PromptFormatter()('{pygitstatus.tag_or_hash}') == 'v1'


def test_tag_or_hash_unannotated(git_repo):
    with cd(git_repo.working_tree_dir):
        git_repo.index.commit('initial commit')
        git_repo.git.tag('v1')
        assert PromptFormatter()('{pygitstatus.tag_or_hash}') == 'v1'


def test_tag_or_hash_hash(git_repo):
    '''No tag, so hash should be resolved'''
    with cd(git_repo.working_tree_dir):
        git_repo.index.commit('initial commit')
        # The OOTB default for git is 7,
        # but this _could_ be affected by a user's core.abbrev setting
        short_head = git_repo.commit().name_rev[:7]

        assert PromptFormatter()('{pygitstatus.tag_or_hash}') == short_head


def test_untracked(git_repo):
    with cd(git_repo.working_tree_dir):
        Path('text.txt').touch()
        assert PromptFormatter()('{pygitstatus.untracked}') == '…1'


def test_pygitstatus(git_repo):
    with cd(git_repo.working_tree_dir):
        base_commit = git_repo.index.commit('initial commit')

        # Stash
        workfile = Path('workfile.txt')
        workfile.touch()
        git_repo.git.stash('--include-untracked')

        # Set up merge conflict
        default_branch = git_repo.active_branch.name
        conflict_file = Path('conflict_file.txt')

        conflict_file.write_text('Hello World!', encoding='utf-8')
        git_repo.git.add(conflict_file)

        # Add file we will delete later
        deleted_file = Path('deleted.txt')
        deleted_file.touch()
        git_repo.git.add(deleted_file)

        # Add file we will change
        changed_file = Path('changed_file.txt')
        changed_file.touch()
        git_repo.git.add(changed_file)

        git_repo.index.commit('m1')

        git_repo.git.checkout(base_commit)
        git_repo.create_head('f1')
        git_repo.git.checkout('f1')
        conflict_file.write_text('Goodbye World!', encoding='utf-8')
        git_repo.git.add(conflict_file)
        git_repo.index.commit('f1')

        # Ahead and behind
        git_repo.git.branch(f'--set-upstream-to={default_branch}')

        # Should error since there is a conflict
        try:
            git_repo.git.merge(default_branch)
        except GitCommandError as err:
            if 'CONFLICT' not in err.stdout:
                raise err from err

        # Changed
        changed_file.write_text('Changed!', encoding='utf-8')

        # Deleted
        deleted_file.unlink()

        # Untracked
        Path('untracked.txt').touch()

        print('> git status && echo ... && git status --porcelain')
        print(git_repo.git.status() + '...' + os.linesep +
              git_repo.git.status('--porcelain'))
        pygitstatus_expected = '{CYAN}f1↑·1↓·1{CYAN}|MERGING{RESET}|{RED}●2{RESET}{RED}×1{RESET}{BLUE}+1{RESET}{RED}-1{RESET}…1⚑1'  # noqa: E501, RUF001
        gitstatus_expected = '{CYAN}f1↑·1↓·1{CYAN}|MERGING{RESET}|{RED}●3{RESET}{BLUE}+1{RESET}{RED}-1{RESET}…1⚑1'  # noqa: E501
        assert PromptFormatter()('{pygitstatus}') == pygitstatus_expected
        assert PromptFormatter()('{gitstatus}') == gitstatus_expected
