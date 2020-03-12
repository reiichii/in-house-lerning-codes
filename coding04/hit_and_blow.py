import sys
from random import randrange

correct_answer = "".join([str(randrange(10)) for i in range(3)])
digit = 3


def validate(val) -> str:
    try:
        user_answer = str(int(val))
    except ValueError:
        print("Invalid Value")

    if len(user_answer) != digit:
        print("Invalid number of digits")
    else:
        return user_answer
    sys.exit


def check_the_answer(user_answer: str) -> bool:
    # hitを探す
    hit = 0
    blow_candidates = ""
    for i in range(digit):
        if correct_answer[i] == user_answer[i]:
            hit += 1
        else:
            blow_candidates += correct_answer[i]

    if hit == digit:
        return True

    # blowを探す
    blow = len(set(list(blow_candidates)).intersection(set(list(user_answer))))

    print(f"{hit}Hit {blow}Blow")


if __name__ == "__main__":
    validate_user_answer = None
    while validate_user_answer != True:
        user_answer = validate(input("Your Number? : "))
        validate_user_answer = check_the_answer(user_answer)
    print("Clear!")