import time
import csv
import os
from os import path
import math
import sys

def print_header():
    os.system('cls')
    header = """
                 __                                                                   __
            ___||    _ _ _    _ _ _    _ _ _   _ _ _   _    _   _ _ _   _ _ _   _ _ _   ||___
        ___|   ||   |  _  \  |  _  \  |  _  | |  _ _| | |  / / |  _ _| |_   _| |  _ _|  ||   |___
       |   |___||   | |_/ /  | |_/ |  | |_| | | |     | | / /  | |_ _    | |   | |_ _   ||___|   |
    ___|       ||   |  _  \  |    /   |  _  | | |     | |/ /   |  _ _|   | |   |_ _  |  ||       |___
       |    ___||   | |  \ \ | |\ \   | | | | | |     | |\ \   | |       | |       | |  ||___    |
       |___|   ||   | |_ / / | | \ \  | | | | | |_ _  | | \ \  | |_ _    | |    _ _| |  ||   |___|
           |___||   |_ _ _/  |_|  \_\ |_| |_| |_ _ _| |_|  \_\ |_ _ _|   |_|   |_ _ _|  ||___|
               ||__                                                                   __||
               """
    print(header)


def print_bracket(tiers, items, rnd):
    print_header()
    row_len = 0
    for i in range(2*len(items.get(0))+1):
        print()
        for j in range(1, tiers+1):
            if j <= rnd+1:
                row_len = max(len(k) for k in items.get(j-1)) + 4
            else:
                row_len = max(len(k) for k in items.get(rnd)) + 4
            k = 2**j
            if i % k == k/2:
                # basic row
                if j <= rnd + 1:
                    print(items.get(j-1)[i//(2**j)].center(row_len, '_'), end="")
                else:
                    print('_'*row_len, end="")
            else:
                # gap indent
                print(" "*row_len, end="")
            if abs(i%(k*2)-(k+0.5)) < k/2:
                # connecting bars
                print("|", end="")
            else:
                # no connection
                print(" ", end="")
        if i % 2**(tiers+1) == 2**tiers:
            # winner's row
            if tiers == rnd:
                print(items.get(rnd)[0].center(row_len, '_'), end ="")
            else:
                print('_'*row_len, end ="")
    print()


def faceoff(x, y):
    print("\n\n" + x + " vs. " + y)
    print("0: " + x)
    print("1: " + y)
    while True:
        print("Winner: ", end="")
        try:
            rounds = int(input())
            if rounds in {0, 1}:
                break
        except Exception:
            pass
    return x if rounds == 0 else y


def main():
    print_header()
    all_items = {}
    orig_items = []

    folder_path = os.path.join(os.path.dirname(__file__), "Items")
    item_files = os.listdir(folder_path)
    print("Welcome to Brackets! Which file would you like to import?")
    for i in range(len(item_files)):
        print(str(i) + ": " + item_files[i])
    while True:
        print("Import select: ", end="")
        try:
            file_select = int(input())
            if file_select in range(len(item_files)):
                break
        except Exception:
            pass

    # Read tournament entries
    file_name = item_files[file_select]
    if file_name.endswith(".txt"):
        with open("Items/" + file_name) as f:
            for line in f:
                orig_items.append(line.strip('\n'))

    elif file_name.endswith(".csv"):
        with open("Items/" + file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                orig_items.append(row['Track Name'])
    else:
        print("Woops! That file format is not supported.")
        exit(0)

    # Calculate number of rounds and insert byes as necessary
    rounds = math.ceil(math.log(len(orig_items), 2))
    for i in range(2**rounds - len(orig_items)):
        orig_items.append('')
    all_items[0] = orig_items

    print("\nGreat! You'll need a " + str(rounds) + "-round tournament.")
    input("Ready to begin? ")

    # Run each round of the tournament
    for i in range(0, rounds):
        curr_items = all_items.get(i)           # Contestants not eliminated
        print_bracket(rounds, all_items, i)     # Print current bracket
        new_items = []

        # Faceoff adjacent contestants
        for j in range(0, len(curr_items), 2):
            if not curr_items[j+1]:
                new_items.append(curr_items[j])
            else:
                new_items.append(faceoff(curr_items[j], curr_items[j+1]))
        all_items[i+1] = new_items

    # Store tournament results
    with open("Results.txt", 'w+') as f:
        orig_stdout = sys.stdout
        sys.stdout = f
        print_bracket(rounds, all_items, rounds)
        sys.stdout = orig_stdout

    print_bracket(rounds, all_items, rounds)

if __name__ == "__main__":
    main()
