import random

vibe_checks = {
    "good": ["Everything’s aligning in your favor today!", "Go take a break- you deserve it :)", "Make sure to appreciate the little things in life!", "Say something nice to someone you appreciate :)"],
    "bad": ["Could be better but that's okay, just hang in there!", "Today's a bit rough, but there's always tomorrow!", "Dont be too harsh on yourself, you are doing great :)"],
    "random": ["Treat yourself, you deserve it!", "Just another day, but nothing wrong with that!", "Another day, another slay B)", "Meow"],
}

def get_vibe_check(vibes):
    if vibes in vibe_checks:
        return random.choice(vibe_checks[vibes])
    else:
        return random.choice(vibe_checks["random"])