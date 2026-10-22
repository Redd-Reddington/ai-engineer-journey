import sys


def is_valid_format(card_number):
    return len(card_number) == 16 and card_number.isascii() and card_number.isdigit()


def format_card_number(card_number):
    return "-".join(card_number[i:i + 4] for i in range(0, 16, 4))


def get_card_type(card_number):
    if card_number.startswith("4"):
        return "VISA"
    if "51" <= card_number[:2] <= "55":
        return "Master Card"
    return "invalid card"


def main():
    card_number = input("Enter your credit card number (should be 16 digits): ").strip()

    if not is_valid_format(card_number):
        print("Invalid card number. Please enter a 16-digit card number.")
        sys.exit(1)

    print("Formatted card number:", format_card_number(card_number))
    print("Card Type:", get_card_type(card_number))


if __name__ == "__main__":
    main()