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

## Development

## Releasing your package

-   Bump the version of your package.
-   Create a GitHub release (The release notes are automatically generated as a draft release after each push).
-   And publish with `poetry publish --build` or `twine`

## Credits

This package was created with [xontrib template](https://github.com/xonsh/xontrib-template).

---

## Xontrib Promotion (DO and REMOVE THIS SECTION)

-   Check that your repository name starts from `xontrib-` prefix. It helps Github search find it.

-   Add `xonsh`, `xontrib` and other thematic topics to the repository "About" setting.

-   Add preview image in "Settings" - "Options" - "Social preview". It allows to show preview image in Github Topics and social networks e.g. Twitter.

-   Enable "Sponsorship" in "Settings" - "Features" - Check "Sponsorships".

-   Add xontrib to the [awesome-xontribs](https://github.com/xonsh/awesome-xontribs).

-   Publish your xontrib to PyPi via Github Actions and users can install your xontrib via `xpip install xontrib-myxontrib`. Easiest way to achieve it is to use Github Actions. Register to https://pypi.org/ and [create API token](https://pypi.org/help/#apitoken). Go to repository "Settings" - "Secrets" and your PyPI API token as `PYPI_API_TOKEN` as a "Repository Secret". Now when you create new Release the Github Actions will publish the xontrib to PyPi automatically. Release status will be in Actions sction. See also `.github/workflows/release.yml`.

-   Write a message to: [xonsh Gitter chat](https://gitter.im/xonsh/xonsh?utm_source=xontrib-template&utm_medium=xontrib-template-promo&utm_campaign=xontrib-template-promo&utm_content=xontrib-template-promo), [Twitter](https://twitter.com/intent/tweet?text=xonsh%20is%20a%20Python-powered,%20cross-platform,%20Unix-gazing%20shell%20language%20and%20command%20prompt.&url=https://github.com//xontrib-pygitstatus), [Reddit](https://www.reddit.com/r/xonsh), [Mastodon](https://mastodon.online/).
