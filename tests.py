def tree_add(tree, dirpath, dirname=None, filename=None):
    if dirpath not in tree:
        tree[dirpath] = ([], [])
    dirnames, filenames = tree[dirpath]
    if dirname is not None and dirname not in dirnames:
        dirnames.append(dirname)
    if filename is not None and filename not in filenames:
        filenames.append(filename)


def build_tree(paths):
    tree = {}
    for path in paths:
        dirpath = ''
        if '/' not in path:
            tree_add(tree, dirpath, filename=path)
            continue
        if not path.endswith('/'):
            path, filename = path.rsplit('/', 1)
            tree_add(tree, path, filename=filename)
        for dirname in path.split('/'):
            tree_add(tree, dirpath, dirname=dirname)
            dirpath = dirpath + ('/' if dirpath else '') + dirname
    return tree


def walk_tree(tree, dirpath):
    dirnames, filenames = tree[dirpath]
    yield dirpath, dirnames, filenames

    for dirname in dirnames:
        for item in walk_tree(tree, '/'.join(filter(None, [dirpath, dirname]))):
            yield item


def walk(paths):
    tree = build_tree(paths)
    for dirpath, dirnames, filenames in walk_tree(tree, ''):
        yield dirpath, dirnames, filenames


def test_walk():
    paths = [
        'a/b/c.txt',
        'a/b/d.txt',
        'a/b/e.txt',
        'a/c.txt',
    ]
    assert list(walk(paths)) == [
        ('', ['a'], []),
        ('a', ['b'], ['c.txt']),
        ('a/b', [], ['c.txt', 'd.txt', 'e.txt']),
    ]
