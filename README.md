# Gambling
This is a basic python program for a gambling game created entirely made by Vishesh Kudva.

## Game Rules

### Game Start
First, each player receives:
- 3x $1 tokens
- 1x $2 tokens
- 1x $5 tokens
- 2x $10 tokens
- 1x $20 tokens
- 1x $50 tokens
- 2x $100 tokens
- 1x $200 tokens
- 2x $500 tokens
- 0x $1k tokens _($1,000)_
- 0x $5k notes _($5,000)_
- 0x $10k notes _($10,000)_
- 0x $20k notes _($20,000)_
- 0x $50k notes _($50,000)_
- 0x $100k notes _($100,000)_

Then, the game begins.

### On Your Turn

#### Calculate Loan Amounts
Before you can even start making bad financial decisions, first you must calculate the interest on your loans.
_(Only if applicable)_

This is calculated as:
```
ceiling(loan amount * 1.05)
```
_If the player is now in debt, they **MUST** take out further loans._

Now, you can start wasting money.

#### Bet
Your first bad decision is the bet amount.
This is any positive integer amount between $1 and $999,999.
Get the required tokens for your bet and place them on the board.

Now, the player must choose a number between 2 and 19.
This will act as the **multiplier** of their bet.
They then roll a **D20** on the board. _(If it rolls off, the roll is invalidated regardless of the number.)_

#### First Roll
This uses a **D20**.
- If their roll is 1, they lose their bet amount and half of their money is removed.
  - We always round down here.
  - _They are no longer eligible for further multipliers._
- If their roll is 20, their win is calculated as such:
  - First, they lose their bet.
  - Then, IF any notes have been collected by any player at any point beforehand, they win a $100k note.
  - Else, they win a $1k token.
  - _They are no longer eligible for further multipliers._
- If their roll is < their selected multiplier, they lose their bet and their turn ends.
  - _They are no longer eligible for further multipliers._
- If their roll is >= their selected multiplier, their winning amount is their selected multiplier * their bet.
  - _They are eligible for further multipliers._

#### Further Rolls
If the player is eligible for further multipliers, they may select the following multiplier options.

##### Basic Multiplier
Once selected, the player can roll a regular **D10** dice.
- If the roll is an even number, the player's winnings are multiplied by 10.
  - They are eligible for further rolls, but the player can choose not to roll and to end their turn here.
- If the roll is an odd number, the player now owes the bank their winnings amount.
  - Their turn ends here, and they do not get their winnings.
  - _If the player is now in debt, they **MUST** take out a loan._

##### Ultra Multiplier
**This multiplier is only available once any player on the board gets a $1k token.**
Once selected, the player can roll a **100x D10** dice.
- If the roll is 20, 40, 60, 80, or 100:
  - The player's winnings are multiplied by their roll.
  - They can continue rolling multiplier dice if wanted.
  - **They are no longer eligible to roll the basic multiplier dice on their turn.**
- If the roll is 10, 30, 50, 70, or 90:
  - The player's winnings are nullified
  - The player now owes the bank their original winnings * their roll.
  - _If the player is now in debt, they **MUST** take out a loan._
  - Their turn is now over.

#### Loans
The player, if they want (or if they have no other choice), may take out a loan at any point of their turn.
The minimum loan amount is $1, and the maximum is $1T. _($1,000,000,000,000)_
The loan is taken from the bank with 5% compound interest per turn.

### How To Win
Once any player gets a net positive value of $1M ($1,000,000), the game ends.
