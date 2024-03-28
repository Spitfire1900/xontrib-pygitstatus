import pygit2

for entry in dir(pygit2):
    if entry.startswith('GIT_'):
        enum_val = getattr(pygit2, entry)
        print(entry + ': ' + str(enum_val))
