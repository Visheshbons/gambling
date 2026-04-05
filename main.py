# Imports and variables
import math
import random

START_VALUE = 1500
WIN_VALUE = 1000000000000
MAX_LOAN = 1000000  # hard cap
LOAN_PERCENT_CAP = 1.5  # 150% of current worth

multiplierD100active = False
dice = False
players = []


class Player:
    def __init__(self, id):
        self.id = id
        self.worth = START_VALUE
        self.loans = []
        self.netWorth = self.worth - sum(self.loans)

    def updateNetWorth(self):
        self.netWorth = self.worth - sum(self.loans)

    def add(self, amount):
        self.worth += amount
        self.updateNetWorth()

    def addLoan(self, amount):
        self.loans.append(amount)
        self.worth += amount
        self.updateNetWorth()

    def payLoan(self, index, amount):
        amount = min(amount, self.loans[index], self.worth)
        self.worth -= amount
        self.loans[index] -= amount

        if self.loans[index] == 0:
            del self.loans[index]

        self.updateNetWorth()

    def loanInterest(self):
        for i in range(len(self.loans)):
            self.loans[i] = math.ceil(self.loans[i] * 1.05)
        self.updateNetWorth()


def init():
    global dice
    print("Welcome to the GAMBLING software!")

    playerCount = int(input("Enter the number of players: "))
    for i in range(playerCount):
        players.append(Player(i))

    dice = input("Are you playing a physical game? (y/n)") == "y"

    if dice:
        print("Give players their tokens...")
        input("Press ENTER once ready.\n")

    main()


def gameOver():
    for p in players:
        if p.netWorth >= WIN_VALUE:
            print(f"Player {p.id + 1} just won! (${p.netWorth})")
            return True
    return False


def handleLoans(p):

    # === CALCULATE MAX LOAN ===
    percent_limit = int(p.worth * LOAN_PERCENT_CAP)
    max_allowed = max(1, min(MAX_LOAN, percent_limit))

    # === FORCE LOAN IF BROKE ===
    if p.worth <= 0:
        percent_limit = int(-p.worth * LOAN_PERCENT_CAP)
        max_allowed = max(1, min(MAX_LOAN, percent_limit))
        print("You have $0! You must take a loan.")
        print(f"Max loan allowed: ${max_allowed}")

        while True:
            amount = int(input("Enter loan amount: "))
            if 1 <= amount <= max_allowed:
                p.addLoan(amount)
                break
            print("Invalid loan amount.")

    # === OPTIONAL LOANS ===
    while True:
        percent_limit = int(p.worth * LOAN_PERCENT_CAP)
        max_allowed = max(1, min(MAX_LOAN, percent_limit))

        choice = input("Take a loan? (y/n): ")
        if choice != "y":
            break

        print(f"Max loan allowed: ${max_allowed}")

        amount = int(input("Enter loan amount: "))
        if 1 <= amount <= max_allowed:
            p.addLoan(amount)
        else:
            print("Invalid loan amount.")

    # === REPAYMENT ===
    while len(p.loans) > 0 and p.worth > 0:
        choice = input("Do you want to repay a loan? (y/n): ")
        if choice != "y":
            break

        for idx, loan in enumerate(p.loans):
            print(f"{idx + 1}: ${loan}")

        try:
            loanIndex = int(input("Select loan number: ")) - 1
            amount = int(input("Enter repayment amount: "))
            p.payLoan(loanIndex, amount)
        except:
            print("Invalid input.")


# Main loop
def main():
    global multiplierD100active

    while not gameOver():
        # Show stats
        for p in players:
            print(f"\nPlayer {p.id + 1} has ${p.worth}")
            if p.loans:
                # Take interest HERE
                p.loanInterest()
                print(f"Loans: {p.loans} (Total: ${sum(p.loans)})")
            print(f"Net: ${p.netWorth}")

        # Player turns
        for p in players:
            print(f"\n--- Player {p.id + 1}'s Turn ---")

            handleLoans(p)

            winnings = 0
            canMultiply = True
            lost = False

            # === VALIDATED BET ===
            while True:
                bet = int(input("Enter your bet amount: "))
                if 1 <= bet <= p.worth:
                    break
                print("Invalid bet! Must be within your current worth.")

            dice1guess = int(input("Enter your number for the d20 (2–19): "))

            # Roll D20
            rolld20 = (
                int(input("Enter d20 amount: ")) if dice else random.randint(1, 20)
            )
            print(f"d20 roll: {rolld20}")

            p.add(-bet)

            # === FIRST ROLL ===
            if rolld20 == 1:
                print("Rolled 1! Lose bet + half money.")
                p.worth //= 2
                p.updateNetWorth()
                continue

            elif rolld20 == 20:
                print("Rolled 20! Jackpot!")
                winnings = 1000
                p.add(winnings)
                multiplierD100active = True
                continue

            elif rolld20 < dice1guess:
                print("You lost your bet.")
                continue

            else:
                winnings = bet * dice1guess
                print(f"You won ${winnings}")

            # === MULTIPLIERS ===
            while canMultiply and input("Use multiplier? (y/n): ") == "y":
                if multiplierD100active:
                    choice = input("d10 or d100: ")
                else:
                    choice = "d10"

                if choice == "d10":
                    roll = int(input("Enter d10: ")) if dice else random.randint(1, 10)
                    print(f"d10: {roll}")

                    if roll % 2 != 0:
                        print("Odd! You lose everything.")
                        p.add(-winnings)
                        lost = True
                        break
                    else:
                        winnings *= 10
                        print(f"Now ${winnings}")

                else:
                    roll = (
                        int(input("Enter d100: "))
                        if dice
                        else random.choice([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
                    )
                    print(f"d100: {roll}")

                    if roll in [10, 30, 50, 70, 90]:
                        loss = winnings * roll
                        print(f"You owe ${loss}")
                        p.add(-loss)
                        lost = True
                        break
                    else:
                        winnings *= roll
                        print(f"Now ${winnings}")

            # === FINAL PAYOUT ===
            if not lost:
                p.add(winnings)

            print(f"End worth: ${p.worth}")


init()
