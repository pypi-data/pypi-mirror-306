from oracle.fortune_cookie import get_fortune, fortunes
    
#test function calls are valid
def test_fortune_cookie():
    result = get_fortune("optimistic")
    assert result in fortunes["optimistic"]

def test_fortune_cookie():
    result = get_fortune("realistic")
    assert result in fortunes["realistic"]

def test_fortune_cookie():
    result = get_fortune("unfortunate")
    assert result in fortunes["unfortunate"]

#tests if all outputs are strings
def test_fortune_is_string():
    result = get_fortune("realistic")
    assert isinstance(result, str)

def test_fortune_is_string():
    result = get_fortune("optimistic")
    assert isinstance(result, str)

def test_fortune_is_string():
    result = get_fortune("unfortunate")
    assert isinstance(result, str)

def test_fortunes_not_empty():
    assert len(fortunes)>0

#tests if invalid argument
def test_default_mood():
    result = get_fortune("invalid_mood")
    assert result in fortunes["optimistic"]