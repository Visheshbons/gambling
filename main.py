# Imports and variables
import math
import random

START_VALUE = 1500
WIN_VALUE = 1000000

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
        self.worth -= amount
        self.loans[index] -= amount
        if self.loans[index] == 0:
            del self.loans[index]
        self.updateNetWorth()


def init():
    print("Welcome to the GAMBLING software!")

    # Get the number of players and save as a constant
    playerCount = int(input("Enter the number of players: "))

    for i in range(playerCount):
        players.append(Player(i))

    if input("Are you playing a physical game? (y/n)") == "y":
        dice = True
    else:
        dice = False

    if dice:
        # Wait until all players have their tokens.
        print("Give players their tokens. Each player should have:")
        print("3x $1 tokens")
        print("1x $2 tokens")
        print("1x $5 tokens")
        print("2x $10 tokens")
        print("1x $20 tokens")
        print("1x $50 tokens")
        print("2x $100 tokens")
        print("1x $200 tokens")
        print("2x $500 tokens")
        input("Press ENTER once all players have their tokens.")

    main()


def gameOver():
    for i in players:
        if players[i].netWorth >= WIN_VALUE:
            print(f"Player {i + 1} just won! (${players[i].netWorth})")
            return True
    # If none return true
    return False


# Main loop
def main():
    while not gameOver():
        # Give all player stats
        for i in players:
            print(f"Player {i + 1} has ${players[i].worth}.")
            if players[i].loans.length > 0:
                print(f"Here are the loans for player {i + 1}:")
                for j in players[i].loans:
                    print(f"Loan {j + 1}: ${players[i].loans[j]}.")
                print(f"Loans total to ${sum(players[i].loans)}.")
            print(f"Net value: {players[i].netWorth}\n")

        for i in players:
            winnings = 0
            bet = int(input("Enter your bet amount: "))
            dice1guess = int(input("Enter your number for the d20: "))

            # D20 roll
            if dice:
                rolld20 = int(input("Enter d20 amount: "))
            else:
                rolld20 = int(math.ceil(random.random() * 20))
                print(f"d20 roll: {rolld20}")

            if dice1guess < rolld20:
                print(f"You lost your bet of ${bet}.")
                return
            # else:
            winnings = bet * dice1guess
            print(f"Your winnings is now {winnings}!")

            # Multipliers
            while input("Would you like to use a multiplier? (y/n): ") == "y":
                if multiplierD100active:
                    multiplierChoice = input("Select between d10 and d100 (d10/d100): ")
                else:
                    multiplierChoice = "d10"

                if multiplierChoice == "d10":
                    if dice:
                        rolld10 = int(input("Enter the roll value: "))
                    else:
                        rolld10 = int(math.ceil(random.random() * 10))
                        print(f"d10 roll: {rolld10}")

                    # If rolld10 is ODD
                    if rolld10 % 2 != 0:
                        print("You lost your money!")
                        winnings = -winnings
                        print(f"You now owe the bank {-winnings}")
                        players[i].add(winnings)
                        print(f"{-winnings} has been removed from your account.")
                        print(f"Your balance is now {players[i].worth}.")
                        if players[i].worth < 0:
                            print(
                                "You are in debt! You now have to take out a loan.\nWe will do this for you."
                            )
                            players[i].addLoan((-winnings))
                    else:  # If rolld10 is EVEN
                        winnings *= 10
                        print(f"Your winnings are now {winnings}!")
                else:  # d100
                    if dice:
                        rolld100 = int(input("Enter the roll value: "))
                    else:
                        rolld100 = int(math.ceil(random.random() * 10) * 10)
                        print(f"d10 roll: {rolld100}")

                    # If rolld100 is 10, 30, 50, 70, or 90
                    if (rolld100 / 100) % 2 != 0:
                        print("Oh no...")
                        winnings = -(winnings * rolld100)
                        print(f"You just lost {-winnings}...")
                        players[i].add(winnings)
                        print(f"Your balance is now {players[i].worth}.")
                        if players[i].worth < 0:
                            print(
                                "You are in debt! You now have to take out a loan.\nWe will do this for you."
                            )
                            players[i].addLoan((-winnings))
                    else:  # If rolld100 is 20, 40, 60, 80, or 100:
                        winnings *= rolld100
                        print(f"Your winnings are now {winnings}!")
            # Player selected "n" for multiplier
            print(f"Your winnings are now {winnings}!")
            players[i].add(winnings)
            print(f"Your worth is now {players[i].worth}!")


init()
