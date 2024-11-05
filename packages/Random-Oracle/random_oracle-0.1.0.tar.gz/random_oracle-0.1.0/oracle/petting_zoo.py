import random

pets = {
    "dog": """ 
    ૮( ˃ ꒳ ˂)ა
    ◟/  づ づ 
    """,
    "cat": """ 
     ╱|、
    (˚ˎ 。7  
    |、˜〵          
    じしˍ,)ノ
    """,
    "rabbit": """
      /) /)
     ( • ༝•)
    c/づ  づ
    """,
    "hamster": "₍ᐢ·͈༝·͈ᐢ₎",
    "goat": """
   ((_))
    > *)     _~
    `;'\\__-'  \\_
        | )  _  ) 
        / / ``w w
       w w
    """,
    "sheep": "໒꒰ྀི ˶• ༝ •˶ ꒱ྀི১",
    "bird": """
    <‘• )
    ( V )
     u—u
    """,
    "frog": "₍𝄐 ̫͡ 𝄐₎", 
    "bear": "ʕっ•ᴥ•ʔっ",
    "fox": """  
      ႔ ႔
    ᠸ^ ^  <
    """
}

def get_random_pet():
    return random.choice(list(pets.values()))
    
def get_pet(pet):
    if pet in pets:
        return pets[pet]
    else:
        return "We don't have that pet in our zoo."