def pytest_itemcollected(item):
    """
    Customizes the node IDs for collected pytest items based on docstrings or class names.

    Args:
        item: Pytest item representing a test function or method.

    Returns:
        None
    """
    par = item.parent.obj if item.parent else None
    node = item.obj if item.obj else None
    
    pref = par.__doc__.strip() if par and par.__doc__ else par.__class__.__name__ if par else None
    suf = node.__doc__.strip() if node and node.__doc__ else node.__name__ if node else None

    if pref or suf:
        item._nodeid = ' '.join(filter(None, (pref, suf)))
