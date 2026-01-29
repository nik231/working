import random
import time


def get_div(n):
    l = []
    for a in range(n+1):
        if n % a == 0:
            l.append(a)

    return random.choice(l)

def main():
    start = time.time()
    operators = ["+","-","/","*"]
    total_questions = 0
    total_correct = 0
    questions = []
    while time.time() - start <= 60:
        a = random.randint(1,100)
        op = random.choice(operators)
        if op == "/":
            b = get_div(a)
        else:
            b = random.randint(1,100)
        a_op_b = f"{a}{op}{b}"
        c = int(eval(a_op_b))

        try:
            answer = int(input(f"{a_op_b}"))
        except:
            answer = ""
        if time.time() - start <= 60:
            if c == answer:
                print(f"This is correct! Time remaining{int(60-(time.time()-start))} seconds")
                total_correct += 1
            else:
                print(f"This is wrong! Time remaining{int(60-(time.time()-start))} seconds")
            total_questions +=1
            questions.append(f"{a_op_b}:{answer}")
    print(f"The number of correct answers {total_correct} out of {total_questions}, at a rate of {total_correct / total_questions * 100}")
    for q in questions:
        print(q)

if __name__ == "__main__":
    main()


