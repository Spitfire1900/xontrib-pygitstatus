# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# # pylint: disable=redefined-outer-name
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
