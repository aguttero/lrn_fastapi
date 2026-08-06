def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 2

def test_is_instance():
    assert isinstance("this is a string", str)
    assert not isinstance("10", int)

def test_boolean():
    validated = True
    assert validated is True
    assert ("hello" == "world") is False

def test_type ():
    assert type("hello") is str
    assert isinstance("hello", str) # same as above, more modern
    assert type("hello" is str) is bool
    assert type("hello" == "hello") is bool
    assert type("hello") is not int
    assert type (1) is int
    assert type ("1" is int) # OJO esto no evalua si "1" es entero...

def test_list():
    num_list = [1,2,3,4,5]
    falsy_list = [0,{},"",[],None,False]
    falsy_any_truly_list = [0,{},"",[],None,False,True]
    any_list = [False, False]
    assert 1 in num_list
    assert 7 not in num_list
#    assert 7 in num_list
    assert all(num_list) # all() evaluates if every single item inside evals to True
    assert not all(falsy_list)
    # assert any (falsy_list)
    assert not any (any_list) # any() evaluates if at least one item evals to True
    assert any (falsy_any_truly_list)
