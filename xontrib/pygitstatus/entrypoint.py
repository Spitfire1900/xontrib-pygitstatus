from xonsh.built_ins import XonshSession

from .prompt import status


def _load_xontrib_(xsh: XonshSession, **_):
    # getting environment variable
    var = xsh.env.get("VAR", "default")

    print("Autoloading xontrib: xontrib-pygitstatus")

    # I don't think I need event_hooks for a PROMPT
    # from .event_hooks import listen_cd
    # xsh.builtins.events.on_chdir(listen_cd)

    prompt_fields = xsh.env.get('PROMPT_FIELDS')
    prompt_fields['pygitstatus'] = status


def _unload_xontrib_(xsh: XonshSession, **kwargs) -> dict:
    """If you want your extension to be unloadable, put that logic here"""
    raise NotImplementedError('unload of pygitstatus not implemented')
