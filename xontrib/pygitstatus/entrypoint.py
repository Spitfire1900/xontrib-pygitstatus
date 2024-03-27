from collections.abc import MutableMapping

from xonsh.built_ins import XonshSession

from .prompt import ahead, behind, branch, clean, repo_path, short_head, tag


def _load_xontrib_(xsh: XonshSession, **_):
    # getting environment variable
    var = xsh.env.get("VAR", "default")

    print("Autoloading xontrib: xontrib-pygitstatus")

    # I don't think I need event_hooks for a PROMPT
    # from .event_hooks import listen_cd
    # xsh.builtins.events.on_chdir(listen_cd)

    prompt_fields: MutableMapping
    prompt_fields = xsh.env.get('PROMPT_FIELDS')  # type: ignore
    prompt_fields['pygitstatus.ahead'] = ahead
    prompt_fields['pygitstatus.behind'] = behind
    prompt_fields['pygitstatus.branch'] = branch
    prompt_fields['pygitstatus.clean'] = clean
    prompt_fields['pygitstatus.repo_path'] = repo_path
    prompt_fields['pygitstatus.short_head'] = short_head
    prompt_fields['pygitstatus.tag'] = tag


def _unload_xontrib_(xsh: XonshSession, **kwargs) -> dict:
    """If you want your extension to be unloadable, put that logic here"""
    raise NotImplementedError('unload of pygitstatus not implemented')
