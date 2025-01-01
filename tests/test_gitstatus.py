# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# # pylint: disable=redefined-outer-name
import pytest
from pygit2.enums import FileStatus

from xontrib.pygitstatus.prompts import __git_status_list


def test__git_status_list_all_basic_statuses():
    assert __git_status_list(32768) == [32768]
    assert __git_status_list(16384) == [16384]
    assert __git_status_list(4096) == [4096]
    assert __git_status_list(2048) == [2048]
    assert __git_status_list(1024) == [1024]
    assert __git_status_list(512) == [512]
    assert __git_status_list(256) == [256]
    assert __git_status_list(128) == [128]
    assert __git_status_list(16) == [16]
    assert __git_status_list(8) == [8]
    assert __git_status_list(4) == [4]
    assert __git_status_list(2) == [2]
    assert __git_status_list(1) == [1]


def test__git_status_list_combination_of_all():
    statuses = [32768, 16384, 4096, 2048, 1024, 512, 256, 128, 16, 8, 4, 2, 1]
    assert __git_status_list(sum(statuses)) == statuses


def build_data(status_array: list[FileStatus]) -> tuple[int, list[int]]:
    return sum(status_array), sorted(status_array, reverse=True)


# status_combinations_data = [
#     build_data([FileStatus.INDEX_MODIFIED,
#                 FileStatus.WT_DELETED]),  # Simple combination
#     build_data([FileStatus.WT_MODIFIED, FileStatus.WT_NEW,
#                 FileStatus.INDEX_NEW]),  # Multiple flags
#     build_data([FileStatus.WT_UNREADABLE,
#                 FileStatus.INDEX_RENAMED]),  # High-value flags
#     build_data([FileStatus.INDEX_TYPECHANGE,
#                 FileStatus.WT_DELETED]),  # Mixed index and working tree flags
# ]

status_combinations_data = [
    # Simple combinations
    build_data([FileStatus.INDEX_MODIFIED,
                FileStatus.WT_DELETED]),  # Index modified and WT deleted
    build_data([FileStatus.WT_MODIFIED, FileStatus.WT_NEW,
                FileStatus.INDEX_NEW]),  # WT modified, new, and index new
    build_data([FileStatus.WT_UNREADABLE,
                FileStatus.INDEX_RENAMED]),  # WT unreadable and index renamed
    build_data([FileStatus.INDEX_TYPECHANGE,
                FileStatus.WT_DELETED]),  # Index typechange and WT deleted

    # Larger combinations
    build_data([
        FileStatus.WT_MODIFIED, FileStatus.WT_NEW, FileStatus.INDEX_NEW,
        FileStatus.INDEX_MODIFIED
    ]),
    build_data([
        FileStatus.WT_DELETED, FileStatus.WT_TYPECHANGE, FileStatus.INDEX_RENAMED,
        FileStatus.INDEX_TYPECHANGE
    ]),

    # Edge cases: testing combinations with higher-value flags
    build_data(
        [FileStatus.WT_UNREADABLE, FileStatus.WT_RENAMED, FileStatus.WT_TYPECHANGE]),
    build_data(
        [FileStatus.WT_UNREADABLE, FileStatus.INDEX_NEW, FileStatus.INDEX_MODIFIED]),

    # All possible statuses combined for a full worktree test
    build_data([
        FileStatus.WT_UNREADABLE, FileStatus.WT_RENAMED, FileStatus.WT_TYPECHANGE,
        FileStatus.WT_DELETED, FileStatus.WT_MODIFIED, FileStatus.WT_NEW,
        FileStatus.INDEX_TYPECHANGE, FileStatus.INDEX_RENAMED, FileStatus.INDEX_DELETED,
        FileStatus.INDEX_MODIFIED, FileStatus.INDEX_NEW
    ]),

    # Minimal status (single flags)
    build_data([FileStatus.WT_MODIFIED]),
    build_data([FileStatus.INDEX_NEW]),
    build_data([FileStatus.WT_DELETED]),
    build_data([FileStatus.INDEX_MODIFIED]),
]


@pytest.mark.parametrize(
    'file_status, expected_statuses', status_combinations_data, ids=[
        f'{file_status} {expected_statuses}'
        for file_status, expected_statuses in status_combinations_data
    ])
def test__git_status_combinations(file_status, expected_statuses):
    assert __git_status_list(file_status) == sorted(expected_statuses, reverse=True)
