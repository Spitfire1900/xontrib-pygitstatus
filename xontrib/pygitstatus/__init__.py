# Xonsh used to use namespace packages as the only supported way to load xontribs, there is still code in older
# versions of Xonsh that sort of expect this.
# When using namespace packages this __init__.py file is loaded if no entrypoint is defined.
#     -- https://xon.sh/tutorial_xontrib.html#structure
