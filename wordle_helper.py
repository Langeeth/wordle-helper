import sys, re
from random import randint

# Higher index = more frequently used word
alphabet = "qjzxvkwyfbghmpduclsntoirae"


def score(word):
    # Lower scores are less frequent words.
    # Words don't benefit from repeating letters
    score = 0
    letters = []
    for c in word:
        if c not in letters:
            score += alphabet.index(c)
        letters.append(c)
    return (word, score)


def rank(words):
    # Rank a list of words by the popularity of the letters in them
    return sorted([score(word) for word in words], reverse=True, key=lambda x: x[1])


def word_matches(pattern, word):
    # Returns true if the word matches the regex pattern
    return bool(re.match(pattern, word))


def has_found_letters(letters_found, word):
    # Returns true if all the letters can be found in the word
    return len([l for l in letters_found if l in word]) == len(letters_found)

def excludes_all_letters(letters, word):
    # Returns True if none of the letters can be found in the word
    return len([l for l in letters if l in word]) == 0

def valid_guess(guess_input):
    return len([l for l in guess_input if l in alphabet]) == 5

def valid_result(result_input):
    return len([l for l in result_input if l in "xYGXyg"]) == 5



if __name__ == "__main__":
    try:
        wordlist = open(sys.argv[1], 'r').read().split("\n")
    except IndexError:
        wordlist = open('5letterwords', 'r').read().split("\n")
    excluded_letters = []
    found_letters = []
    guessed_letters = ""
    solution = list(".....")
    result = "xxxxx"
    while result != "GGGGG" and result != "ggggg":
        for i in range(len(solution)):
            if solution[i] not in alphabet and (len(excluded_letters) + len(found_letters) > 0):
                exclude_here = excluded_letters + [l[0] for l in found_letters if l[1] == i]
                solution[i] = "[^{}]".format("".join(exclude_here))
        solution_regex = "^" + ("".join(solution)) + "$"
        print("Current Solution:\t{}\n".format(solution_regex))
        print("Discovered Letters:\t{}\n".format(", ".join([f[0] for f in found_letters])))
        print("Excluded Letters:\t{}\n".format(", ".join(excluded_letters)))

        # Words that fit what is known about the word so far
        top_matching_words = rank([w for w in wordlist if
                                   word_matches(solution_regex, w)
                                   and has_found_letters([f[0] for f in found_letters], w)])[:10]

        # Words that will eliminate as many new letters as possible, even if it's wrong
        intel_words = rank([w for w in wordlist if excludes_all_letters(guessed_letters, w)])[:5]
        print("{} Suggested Guesses:".format(len(top_matching_words)))
        for tmw in top_matching_words:
            print(tmw)

        print("""
{} Words Excluding All Letters
You Have Already Tried:""".format(len(intel_words)))
        for iw in intel_words:
            print(iw)
        guess = ""
        while not valid_guess(guess):
            guess = input("Input your Guess (5 lowercase letters): ")
        guessed_letters += guess
        result = ""
        while not valid_result(result):
            result = input("What was the result?\n(x for letter not found,\nG for green\nY for yellow): ")
        for i in range(5):
            g = guess[i]
            r = result[i]
            if r == "G" or r == "g":
                solution[i] = g
            if r == "Y" or r == "y":
                found_letters.append((g, i))
            if r == "x" or r == "X":
                excluded_letters.append(g)
