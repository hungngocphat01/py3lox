def stringify(obj: object):
    s = str(obj)
    if isinstance(obj, float):
        s.endswith(".0")
        s = s[:s.find(".0")]
    return s
