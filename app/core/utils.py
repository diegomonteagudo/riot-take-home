
def sort_dict(obj):
    """ Recursively sort dictionary keys at all depths.
    Warning : lists are not sorted, but any dictionaries inside those lists will be sorted."""
    if isinstance(obj, dict):
        return {k: sort_dict(v) for k, v in sorted(obj.items())}
    elif isinstance(obj, list):
        return [sort_dict(item) for item in obj]
    else:
        return obj