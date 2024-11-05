import random

fortunes = {
    "optimistic": ["You will get straight As!", "You will win the lottery."],
    "realistic": ["You will find love soon.", "You will ace that test."],
    "unfortunate": ["You will trip and fall", "A bug will fall in your coffee"]
}

def get_fortune(mood):
    if mood in fortunes:
        return random.choice(fortunes[mood])
    else:
        return random.choice(fortunes["optimistic"])