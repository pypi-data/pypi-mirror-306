from oracle.vibe_check import get_vibe_check, vibe_checks
    
#test function calls are valid
def test_vibe_check():
    result = get_vibe_check("good")
    assert result in vibe_checks["good"]

def test_vibe_check():
    result = get_vibe_check("bad")
    assert result in vibe_checks["bad"]

def test_vibe_check():
    result = get_vibe_check("random")
    assert result in vibe_checks["random"]

#tests if all outputs are strings
def test_vibe_is_string():
    result = get_vibe_check("good")
    assert isinstance(result, str)

def test_vibe_is_string():
    result = get_vibe_check("bad")
    assert isinstance(result, str)

def test_vibe_is_string():
    result = get_vibe_check("random")
    assert isinstance(result, str)

def test_vibe_not_empty():
    assert len(vibe_checks)>0

#tests if invalid argument
def test_default_vibe():
    result = get_vibe_check("invalid_mood")
    assert result in vibe_checks["random"]