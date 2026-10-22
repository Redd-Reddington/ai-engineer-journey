import random

CHOICES = ("rock", "paper", "scissors")
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}  # key beats value
MESSAGES = {"player": "You win!", "computer": "You lost!", "draw": "It's a tie!"}


def get_winner(player, computer):
    if player == computer:
        return "draw"
    return "player" if BEATS[player] == computer else "computer"


def display_results(player, computer, result):
    print(f"You chose: {player}")
    print(f"Computer chose: {computer}")
    print(MESSAGES[result])


def main():
    scores = {"player": 0, "computer": 0, "draw": 0}

    while True:
        player = input("Enter your choice (rock/paper/scissors/quit): ").strip().lower()

        if player == "quit":
            break
        if player not in CHOICES:
            print("Invalid choice. Please choose 'rock', 'paper' or 'scissors'.")
            continue

        computer = random.choice(CHOICES)
        result = get_winner(player, computer)
        display_results(player, computer, result)
        scores[result] += 1

        print("Scores:")
        print(f"WINS: {scores['player']}")
        print(f"LOSES: {scores['computer']}")
        print(f"DRAWS: {scores['draw']}")


if __name__ == "__main__":
    main()