# Unused
import sys


def activate_env(path: str):
    # lazy import to reduce startup cost
    from xontrib.voxapi import Vox

    vox = Vox()
    # print('Path: %s' % path, file=sys.stderr)
    vox.activate(path)


def listen_cd(olddir, newdir, **_):
    '''Honors on_chdir Protocol:
    https://xon.sh/events.html#on-chdir
    '''
    activate_env(newdir)
