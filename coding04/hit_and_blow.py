import sys
from random import randrange
from collections import Counter

QUESTION = "".join([str(randrange(10)) for i in range(3)])
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

def inspect_hit(answer: str) -> str:
    hit = ""
    mismatch = ""
    for i in range(DIGIT):
        if QUESTION[i] == answer[i]:
            hit += QUESTION[i]
        else:
            mismatch += QUESTION[i]
    return hit, mismatch

def inspect_blow(answer: str, mismatch: str) -> str:
    d = set(list(mismatch))
    a = set(list(answer))
    blow = d.intersection(a)
    return ''.join(list(blow))

if __name__ == "__main__":
    hit = ''
    while len(hit) != DIGIT:
        answer = validate(input("Your Number? : "))
        hit, mismatch = inspect_hit(answer)
        blow = inspect_blow(mismatch, answer)
        print(f"{len(hit)}Hit {len(blow)}Blow")
    print("Clear!")