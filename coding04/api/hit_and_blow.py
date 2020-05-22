from random import randrange

DIGIT = 3
QUESTION = ""


def create_question():
    global QUESTION
    QUESTION = "".join([str(randrange(10)) for i in range(DIGIT)])


def validate(val: str) -> bool:
    if val.isdigit() and len(val) == DIGIT:
        return True


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
    return "".join(list(blow))


def check_the_answer(input):
    print(f"Q: {QUESTION}")
    print(f"input:{input}")
    if not validate(input):
        return 0, 0
    hit, mismatch = inspect_hit(input)
    print(f"hit:{hit}")
    blow = inspect_blow(mismatch, input)
    return len(hit), len(blow)


if __name__ == "__main__":
    hit = ''
    answer = validate(input())
    if not answer:
        print("error")
        sys.exit()
    hit, mismatch = inspect_hit(answer)
    blow = inspect_blow(mismatch, answer)
    print(f"{hit} {blow}")
