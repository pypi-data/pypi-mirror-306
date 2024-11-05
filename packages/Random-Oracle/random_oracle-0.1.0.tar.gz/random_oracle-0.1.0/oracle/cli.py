import sys
from fortune_cookie import get_fortune
from eight_ball import get_eight_ball
from vibe_check import get_vibe_check
from petting_zoo import get_random_pet
from petting_zoo import get_pet

def error_msg():
    print("To contact the oracle, type:")
    print("fortune_cookie <mood> to receive your fortune (e.g. optimistic, realistic, unfortunate)")
    print("eight_ball <numOfDecisions> to make a decision")
    print("petting_zoo to feed your pet")
    print("vibe_check to see what's up")


def main():
    if len(sys.argv) == 1:
        error_msg()
        return
    
    command = sys.argv[1].lower()

    if command == "fortune_cookie":
        if len(sys.argv) == 3:
            mood = sys.argv[2].lower()
            print(get_fortune(mood))
        else:
            print("please specify a mood: optimistic, realistic, unfortunate")
            error_msg()
    elif command == "eight_ball":
        if(len(sys.argv) == 3):
            numOfResponses = sys.argv[2]
            if(numOfResponses.isdigit()):
                print(get_eight_ball(numOfResponses))
            else:
                print("please enter a number")
        else:
            print(get_eight_ball(1))
    elif command == "petting_zoo":
        if(len(sys.argv) == 3):
            pet = sys.argv[2].lower()
            print(get_pet(pet))
        else: 
            print(get_random_pet())
    elif command == "vibe_check":
        if len(sys.argv) == 3:
            vibe = sys.argv[2].lower()
            print(get_vibe_check(vibe))
        else:
            print("please specify a vibe: good, bad, or random")
            error_msg()
    else:
        error_msg()

if __name__ == "__main__":
    main()