from sets import Set

def f1(seq): # Raymond Hettinger
    # not order preserving
    set = {}
    map(set.__setitem__, seq, [])
    return set.keys()

    
def f2(seq):   # *********
    # order preserving
    checked = []
    for e in seq:
        if e not in checked:
            checked.append(e)
    return checked

def f3(seq):
    # Not order preserving
    keys = {}
    for e in seq:
        keys[e] = 1
    return keys.keys()

def f4(seq): # ********** order preserving
    noDupes = []
    [noDupes.append(i) for i in seq if not noDupes.count(i)]
    return noDupes

def f5(seq, idfun=None): # Alex Martelli ******* order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result


def f5b(seq, idfun=None): # Alex Martelli ******* order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker not in seen:
            seen[marker] = 1
            result.append(item)
            
    return result



def f6(seq):
    # Not order preserving
    return list(Set(seq))

def f7(seq):
    # Not order preserving
    return list(set(seq))

def f8(seq): # Dave Kirby
    # Order preserving
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

def f9(seq):
    # Not order preserving
    return {}.fromkeys(seq).keys()

def f10(seq, idfun=None): # Andrew Dalke
    # Order preserving
    return list(_f10(seq, idfun))

def _f10(seq, idfun=None):
    seen = set()
    if idfun is None:
        for x in seq:
            if x in seen:
                continue
            seen.add(x)
            yield x
    else:
        for x in seq:
            x = idfun(x)
            if x in seen:
                continue
            seen.add(x)
            yield x
            
            
def f11(seq): # f10 but simpler
    # Order preserving
    return list(_f10(seq))

def _f11(seq):
    seen = set()
    for x in seq:
        if x in seen:
            continue
        seen.add(x)
        yield

