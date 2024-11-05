from oracle.petting_zoo import get_random_pet, get_pet, pets

def test_get_random_pet():
    result = get_random_pet()
    assert result in pets.values()
    
def test_get_pet_exists():
    result = get_pet("hamster")
    assert result == "₍ᐢ·͈༝·͈ᐢ₎"

def test_get_pet_not_exists():
    result = get_pet("dinosaur")
    assert result == "We don't have that pet in our zoo."
