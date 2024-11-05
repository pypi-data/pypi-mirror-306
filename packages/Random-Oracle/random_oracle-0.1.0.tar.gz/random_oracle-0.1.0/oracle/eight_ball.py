import random

responses = [
    "It is certain", 
    "It is decidedly so", 
    "Without a doubt", 
    "Yes definitely", 
    "You may rely on it", 
    "As I see it, yes", 
    "Most likely", 
    "Outlook good", 
    "Yes", 
    "Signs point to yes", 
    "Reply hazy, try again", 
    "Ask again later", 
    "Better not tell you now", 
    "Cannot predict now", 
    "Concentrate and ask again", 
    "Don't count on it", 
    "My reply is no", 
    "My sources say no", 
    "Outlook not so good", 
    "Very doubtful"
]

def get_eight_ball(num):  
    str = ""
    numOfResponses = int(num)
    for i in range(numOfResponses):
        str += random.choice(responses)
        if(i != numOfResponses - 1):
            str += "\n"
    return str