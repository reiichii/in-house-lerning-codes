import sys
from random import randrange
from collections import Counter

CORRECT_ANSWER = "".join([str(randrange(10)) for i in range(3)])
DIGIT = 3


def validate(val) -> str:
    try:
        val = str(int(val))
    except ValueError:
        print("Invalid Value")
        sys.exit()

    if len(val) != DIGIT:
        print("Invalid number of digits")
        sys.exit()
    else:
        return val


def check_the_answer(user_answer: str) -> bool:
    # hitを探す
    hit = 0
    blow_candidates = ""
    for i in range(DIGIT):
        if CORRECT_ANSWER[i] == user_answer[i]:
            hit += 1
        else:
            blow_candidates += CORRECT_ANSWER[i]
    if hit == DIGIT:
        return True

    # blowを探す
    blow = len(list((Counter(list(blow_candidates)) & Counter(list(user_answer))).elements()))

    print(f"{hit}Hit {blow}Blow")


if __name__ == "__main__":
    validate_user_answer = None
    while validate_user_answer != True:
        user_answer = validate(input("Your Number? : "))
        validate_user_answer = check_the_answer(user_answer)
    print("Clear!")