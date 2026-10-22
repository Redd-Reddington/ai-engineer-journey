import random

WORD_BANK = ["java", "hangman", "programming", "assignment"]
MAX_INCORRECT = 6
HANGMAN_STAGES = [
    "",
    " O ",
    " O \n | ",
    " O \n/| ",
    " O \n/|\\",
    " O \n/|\\ \n/ ",
    " O \n/|\\ \n/ \\",
]


class HangmanGame:
    def __init__(self):
        self.start_new_game()

    def start_new_game(self):
        self.word = random.choice(WORD_BANK)
        self.guessed = set()
        self.attempts_left = MAX_INCORRECT

    @property
    def displayed_word(self):
        return " ".join(c if c in self.guessed else "_" for c in self.word)

    @property
    def is_win(self):
        return set(self.word) <= self.guessed

    @property
    def is_loss(self):
        return self.attempts_left <= 0

    def display_hangman(self):
        print(HANGMAN_STAGES[MAX_INCORRECT - self.attempts_left])
        print(f"Guesses left: {self.attempts_left}")

    def guess_letter(self, letter):
        if letter in self.guessed:
            print("You already guessed that letter.")
            return
        self.guessed.add(letter)
        if letter in self.word:
            print("Good Guess!")
        else:
            print("Wrong Guess")
            self.attempts_left -= 1


def play_round(game):
    while not (game.is_win or game.is_loss):
        print("Word to guess:", game.displayed_word)
        guess = input("Guess a letter: ").strip().lower()[:1]
        if not guess.isalpha():
            print("Please enter a letter.")
            continue
        game.guess_letter(guess)
        game.display_hangman()

    if game.is_win:
        print(f"Congratulations! You've guessed the word: {game.word}")
    else:
        print(f"You've lost. The word was: {game.word}")


def main():
    print("Welcome To Hangman!\n")
    game = HangmanGame()
    while True:
        play_round(game)
        if input("Play again? (y/n): ").strip().lower() != "y":
            break
        game.start_new_game()
    print("Thanks for playing!")


if __name__ == "__main__":
    main()