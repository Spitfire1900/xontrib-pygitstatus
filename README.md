<p align="center">
PyGit2 implementation of the builtin gitstatus PROMPT fields.
</p>

xontrib-pygitstatus provides a set of PROMPT fields that mimic the behavior of the builtin gitstatus prompt fields with [minor differences](#differences-from-gitstatus).

Unlike the builtin prompt, xontrib-pygitstatus does not invoke the git cli, so may be more performant in the following cases:

-   You're on a Windows workstations, where process spawning is slower than Linux
-   You have an on-access virtus scanner installed, which will slow down git cli invocations
-   Git is not installed on your system

## Installation

To install use pip:

```xsh
xpip install xontrib-pygitstatus
# or: xpip install -U git+https://github.com//xontrib-pygitstatus
```

## Usage

This xontrib will get loaded automatically for interactive sessions.
To stop this, set

```xsh
$XONTRIBS_AUTOLOAD_DISABLED = ["pygitstatus", ]
# if you have set this for other xontribs, you should append the vale
```

then use pygitstatus's prompts in your .xonshrc file:

```xsh
PROMPT = '{pygitstatus}'
```

Example modified default prompt:

```xsh
$PROMPT = '{YELLOW}{env_name}{RESET}{BOLD_GREEN}{user}@{hostname}{BOLD_BLUE} {cwd}{pygitstatus.branch_color}{pygitstatus_curr_branch: {}}{RESET} {RED}{last_return_code_if_nonzero:[{BOLD_INTENSE_RED}{}{RED}] }{RESET}{BOLD_BLUE}{prompt_end}{RESET}'
```

## Differences from gitstatus

PyGitStatus is a fork of [gitstatus](https://github.com/xonsh/xonsh/blob/0.12.5/xonsh/prompt/gitstatus.py) that nearly follows the same logic as the original gitstatus prompt, but with a few differences:

-   Conflict files are intentionally excluded from pygitstatus.staged.
-   The pygitstatus prompt will include conflicted files when both are added to the index and the working tree.

## Fields

```xsh
{pygitstatus}
{pygitstatus_curr_branch}
{pygitstatus.ahead}
{pygitstatus.behind}
{pygitstatus.branch}
{pygitstatus.branch_bg_color}
{pygitstatus.branch_color}
{pygitstatus.changed}
{pygitstatus.clean}
{pygitstatus.conflicts}
{pygitstatus.deleted}
{pygitstatus.lines_added}
{pygitstatus.lines_deleted}
{pygitstatus.numstat}
{pygitstatus.operations}
{pygitstatus.repo_path}
{pygitstatus.short_head}
{pygitstatus.staged}
{pygitstatus.stash_count}
{pygitstatus.tag}
{pygitstatus.tag_or_hash}
{pygitstatus.untracked}
```

## Known issues

While this xontrib works on Windows, the tests do not pass on Windows.

## Credits

This package was created with [xontrib template](https://github.com/xonsh/xontrib-template).
