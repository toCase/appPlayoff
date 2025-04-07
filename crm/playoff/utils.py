from math import ceil

ROW_COUNT:int = 16

def page_list(_size :int):
    _pages :int = ceil(_size / ROW_COUNT)
    _res = []
    for i in range(1, _pages + 1):
        _res.append(str(i))
    return _res

def page_from(_page :int):
    _from :int = (_page - 1) * ROW_COUNT
    return _from

def page_to(_page :int):
    _to :int = (_page - 1) * ROW_COUNT + ROW_COUNT
    return _to

def error_messages(errors:dict):
    messages = []
    for key in errors.keys():            
        l = errors.get(key)
        for x in l:
            messages.append(x.get("message"))
    return messages