```python
'gitstatus.repo_path': <Prompt: gitstatus.repo_path>, # DONE
'gitstatus.short_head': <Prompt: gitstatus.short_head>, # DONE
'gitstatus.tag': <Prompt: gitstatus.tag>, # DONE
'gitstatus.tag_or_hash': <Prompt: gitstatus.tag_or_hash>, # DONE
'gitstatus.stash_count': <Prompt: gitstatus.stash_count>, # DONE
'gitstatus.operations': <Prompt: gitstatus.operations>, # NA: No subprocess calls used
'gitstatus.porcelain': <Prompt: gitstatus.porcelain>, # TODO
'gitstatus.branch': <Prompt: gitstatus.branch>, # DONE
'gitstatus.ahead': <Prompt: gitstatus.ahead>, # DONE
'gitstatus.behind': <Prompt: gitstatus.behind>, # DONE
'gitstatus.untracked': <Prompt: gitstatus.untracked>, # DONE
'gitstatus.changed': <Prompt: gitstatus.changed>, # DONE
'gitstatus.deleted': <Prompt: gitstatus.deleted>, # DONE
'gitstatus.conflicts': <Prompt: gitstatus.conflicts>, # DONE
'gitstatus.staged': <Prompt: gitstatus.staged>, # DONE
'gitstatus.numstat': <Prompt: gitstatus.numstat>, # DONE
'gitstatus.lines_added': <Prompt: gitstatus.lines_added>, # DONE
'gitstatus.lines_removed': <Prompt: gitstatus.lines_removed>, # DONE
'gitstatus.clean': <Prompt: gitstatus.clean>, # DONE
'gitstatus': <Prompt: gitstatus>, # DONE
```

-   currbranch <!--
        DONE: Bug with prompt_bar.
        when referencing pygitstatus.branch I get a KeyError.
        Adding a new pygitstatus_branch prompt avoids this but it
        is only inferred if it is also in the PROMPT.
        In addition it only correctly displays on n+1 prompts, not the next prompt.
        -->
-   branch_color <!-- TODO  -->
-   ALL Prompts need the name field set. <!-- DONE  -->
-   Prompts like deleted, changed, etc. need to consider that status() combines the INDEX and WT status <!-- DONE  -->

    ```python
    """
    GIT_STATUS_INDEX_DELETED: 4
    GIT_STATUS_INDEX_MODIFIED: 2
    GIT_STATUS_INDEX_NEW: 1
    GIT_STATUS_INDEX_RENAMED: 8
    GIT_STATUS_INDEX_TYPECHANGE: 16
    GIT_STATUS_WT_DELETED: 512
    GIT_STATUS_WT_MODIFIED: 256


    GIT_STATUS_WT_NEW: 128
    GIT_STATUS_WT_RENAMED: 2048
    GIT_STATUS_WT_TYPECHANGE: 1024
    GIT_STATUS_WT_UNREADABLE: 4096
    """
    @ Repo('.').status()
    {'pygit2_status_codes.py': 128,
    'TODO.md': 2,
    'xontrib/pygitstatus/entrypoint.py': 258,
    'xontrib/pygitstatus/prompts.py': 258}
    ```
