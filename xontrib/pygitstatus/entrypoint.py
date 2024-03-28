from collections.abc import MutableMapping

from xonsh.built_ins import XonshSession

from .prompts import (ahead, behind, branch, changed, clean, repo_path, short_head, stash_count, tag, untracked)


def _load_xontrib_(xsh: XonshSession, **_) -> dict:
    """
    this function will be called when loading/reloading the xontrib.

    Args:
        xsh: the current xonsh session instance, serves as the interface to manipulate the session.
             This allows you to register new aliases, history backends, event listeners ...
        **kwargs: it is empty as of now. Kept for future proofing.
    Returns:
        dict: this will get loaded into the current execution context
    """

    # getting environment variable
    var = xsh.env.get('VAR', 'default')

    print('Autoloading xontrib: xontrib-pygitstatus')

    # I don't think I need event_hooks for a PROMPT
    # from .event_hooks import listen_cd
    # xsh.builtins.events.on_chdir(listen_cd)

    prompt_fields: MutableMapping
    prompt_fields = xsh.env.get('PROMPT_FIELDS')  # type: ignore
    prompt_fields['pygitstatus.ahead'] = ahead
    prompt_fields['pygitstatus.behind'] = behind
    prompt_fields['pygitstatus.branch'] = branch
    prompt_fields['pygitstatus.changed'] = changed
    prompt_fields['pygitstatus.clean'] = clean
    prompt_fields['pygitstatus.repo_path'] = repo_path
    prompt_fields['pygitstatus.short_head'] = short_head
    prompt_fields['pygitstatus.stash_count'] = stash_count
    prompt_fields['pygitstatus.tag'] = tag
    prompt_fields['pygitstatus.untracked'] = untracked
    return {}


def _unload_xontrib_(xsh: XonshSession, **kwargs) -> dict:
    """
    If you want your extension to be unloadable, put that logic here

    Args:
        xsh: the current xonsh session instance, serves as the interface to manipulate the session.
             This allows you to register new aliases, history backends, event listeners ...
        **kwargs: it is empty as of now. Kept for future proofing.
    Returns:
        dict: this will get loaded into the current execution context
    """

    prompt_fields: MutableMapping
    prompt_fields = xsh.env.get('PROMPT_FIELDS')  # type: ignore
    key: str
    for key in list(prompt_fields.keys()):
        if key.startswith('pygitstatus'):
            del prompt_fields[key]
    return {}
