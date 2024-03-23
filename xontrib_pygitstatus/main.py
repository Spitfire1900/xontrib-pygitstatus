from xonsh.built_ins import XonshSession


def _load_xontrib_(xsh: XonshSession, **_):
    # getting environment variable
    var = xsh.env.get("VAR", "default")

    print("Autoloading xontrib: xontrib-pygitstatus")

    from .event_hooks import listen_cd
    xsh.builtins.events.on_chdir(listen_cd)

def _unload_xontrib_(xsh: XonshSession, **kwargs) -> dict:
    """If you want your extension to be unloadable, put that logic here"""
    raise NotImplementedError('unload of pygitstatusnot implemented')
