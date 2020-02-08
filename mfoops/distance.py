from functools import lru_cache


# how many edits (insert, delete, modify) are needed to turn s0 into s1?
@lru_cache(maxsize=None)
def edit_distance(s0, s1):
    # if either is empty, number of edits is remaining length of non-empty string
    if len(s0) == 0 or len(s1) == 0:
        return len(s0) + len(s1)

    # no edit needed
    if s0[0] == s1[0]:
        return edit_distance(s0[1:], s1[1:])

    return 1 + min(
        edit_distance(s0, s1[1:]), # insert: s1[0] + s0
        edit_distance(s0[1:], s1), # delete
        edit_distance(s0[1:], s1[1:]) # modify: s0[0] = s1[0]
    )
    

def test_edit_distance():
    # base
    assert edit_distance("", "") == 0 # empty
    assert edit_distance("edit", "edit") == 0 # not empty

    # insert
    assert edit_distance("", "a") == 1 # base
    assert edit_distance("b", "ab") == 1 # before
    assert edit_distance("a", "ab") == 1 # after
    assert edit_distance("ac", "abc") == 1 # between
    assert edit_distance("", "ab") == 2 # twice, base
    assert edit_distance("c", "abc") == 2 # twice, before
    assert edit_distance("a", "abc") == 2 # twice, after
    assert edit_distance("b", "abc") == 2 # twice, around
    assert edit_distance("ad", "abcd") == 2 # twice, between
    assert edit_distance("ace", "abcde") == 2 # twice, spread
    
    # delete
    assert edit_distance("a", "") == 1 # base
    assert edit_distance("ab", "b") == 1 # before
    assert edit_distance("ab", "a") == 1 # after
    assert edit_distance("abc", "ac") == 1 # between
    assert edit_distance("ab", "") == 2 # twice, base
    # delete twice before == insert twice before
    # delete twice after == insert twice after
    assert edit_distance("abc", "b") == 2 # twice, around
    assert edit_distance("abcd", "ad") == 2 # twice, between
    assert edit_distance("abcde", "ace") == 2 # twice, spread

    # modify (aka, insert + delete or delete + insert)
    assert edit_distance("a", "b") == 1 # base
    assert edit_distance("xb", "yb") == 1 # before
    assert edit_distance("ax", "ay") == 1 # after
    assert edit_distance("axc", "ayc") == 1 # between
    assert edit_distance("xx", "yy") == 2 # twice, base
    assert edit_distance("xxb", "yyb") == 2 # twice, before
    assert edit_distance("axx", "ayy") == 2 # twice, after
    assert edit_distance("xbx", "yby") == 2 # twice, around
    assert edit_distance("axxc", "ayyc") == 2 # twice, between
    assert edit_distance("axbxc", "aybyc") == 2 # twice, spread

    # insert + modify and mondify + insert
    assert edit_distance("x", "yb") == 2

    # delete + modify
    assert edit_distance("abc", "bd") == 2

    # modify + modify
    assert edit_distance("xbx", "yby") == 2
    assert edit_distance("axxd", "ayyd") == 2
    assert edit_distance("axcxe", "aycye") == 2

    # delete + insert + modify == modify twice
    # insert + delete + modify == modify twice
    
    # extra   
    assert edit_distance("edit", "") == edit_distance("", "edit") == 4
    assert edit_distance("hello", "hail") == edit_distance("hail", "hello") == 3
    assert edit_distance("intrinsic", "intrusive") == 4
