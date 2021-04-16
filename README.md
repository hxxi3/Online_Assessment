# Online_Assessment

## Description

This program implements basic requirements of ATM with following instructions.

At least the following flow should be implemented:

Insert Card => PIN number => Select Account => See Balance/Deposit/Withdraw

For simplification, there are only 1 dollar bills in this world, no cents. Thus account balance can be represented in integer.

Your code doesn't need to integrate with a real bank system, but keep in mind that we may want to integrate it with a real bank system in the future. It doesn't have to integrate with a real cash bin in the ATM, but keep in mind that we'd want to integrate with that in the future. And even if we integrate it with them, we'd like to test our code. Implementing bank integration and ATM hardware like cash bin and card reader is not a scope of this task, but testing the controller part (not including bank system, cash bin etc) is within the scope.

A bank API wouldn't give the ATM the PIN number, but it can tell you if the PIN number is correct or not.

Based on your work, another engineer should be able to implement the user interface. You don't need to implement any REST API, RPC, network communication etc, but just functions/classes/methods, etc.

You can simplify some complex real world problems if you think it's not worth illustrating in the project.

## Build and tests

`python3 atm.py`

in order to test custom user input, please use 

`python3 atm.py --use-user-input=true`

## List of available commands

1. add_card card_number
- simulates inserting card into ATM
2. authenticate pin_number
- authenticate card with given pin
3. withdrawal amount
4. deposit amount
5. get_balance
6. list_account
- show list of registered accounts on card
7. select_account account_number
- select account with account_number
8. eject
- simulates ejecting card from ATM

## Limitation and future work

1. Synchronization
- This program cannot be used in multi-threaded environment, as synchronization is not introduced

2. Fine-graded authentication
- As this program is for POC, fine-graded authentication such as maintaining session is not included

3. Input abstraction
- This program takes stdin user input, and input abstraction (using network packet, ...) is not included
