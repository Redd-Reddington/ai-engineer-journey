import random
import threading
from dataclasses import dataclass

QUESTIONS_PER_QUIZ = 5
TIME_LIMIT = 15
POINTS_CORRECT = 2
POINTS_WRONG = -1


@dataclass(frozen=True)
class Question:
    text: str
    options: list[str]
    answer: str  # the correct option's text, so no off-by-one index to track


QUESTION_BANK = [
    Question("What is the capital of France?", ["Paris", "London", "Berlin", "Madrid"], "Paris"),
    Question("What is the square root of 25?", ["3", "5", "6", "7"], "5"),
    Question("Who developed Java programming language?",
             ["James Gosling", "Dennis Ritchie", "Bjarne Stroustrup", "Guido van Rossum"], "James Gosling"),
    Question("What currency does Ghana use?", ["Dollar", "Pounds", "Cedi", "Shilling"], "Cedi"),
    Question("How many genders exist?", ["1", "2", "3", "Many more"], "2"),
    Question("Manchester United was most successful under?",
             ["Jose Mourinho", "David Moyes", "Erik Ten Hag", "Louis Van Gaal"], "Jose Mourinho"),
    Question("All that glitters is not?", ["Diamond", "Money", "Oil", "Gold"], "Gold"),
    Question("Common sense is not common to?",
             ["Rich People", "Expensive People", "Wise People", "Common People"], "Common People"),
    Question("What is created in God's image?", ["Lion", "Birds", "Man", "Trees"], "Man"),
    Question("What is the fastest animal?", ["Tiger", "Lion", "Cheetah", "Zebra"], "Cheetah"),
]


def input_with_timeout(prompt, seconds):
    """Return the user's reply, or None if they don't answer in time."""
    reply = []
    thread = threading.Thread(target=lambda: reply.append(input(prompt)), daemon=True)
    thread.start()
    thread.join(seconds)
    return reply[0] if reply else None


def ask_question(question):
    print(question.text)
    for number, option in enumerate(question.options, start=1):
        print(f"{number}. {option}")

    reply = input_with_timeout(f"You have {TIME_LIMIT} seconds to answer... ", TIME_LIMIT)
    if reply is None:
        print("\nTimeout! Moving to the next question.")
        return False

    try:
        choice = int(reply)
    except ValueError:
        choice = 0
    if not 1 <= choice <= len(question.options):
        print("Invalid input. Moving to the next question.")
        return False

    return question.options[choice - 1] == question.answer


def update_leaderboard(scores, name, score):
    scores[name] = score
    for player, points in sorted(scores.items(), key=lambda item: item[1], reverse=True):
        print(f"{player}: {points} points")


def main():
    score = 0
    for question in random.sample(QUESTION_BANK, QUESTIONS_PER_QUIZ):
        if ask_question(question):
            score += POINTS_CORRECT
            print("Correct!")
        else:
            score += POINTS_WRONG
            print("Incorrect!")

    print(f"Quiz Completed!\nYour total score: {score}")
    update_leaderboard({}, "You", score)


if __name__ == "__main__":
    main()