import copy

# Exercise 1 - Iris Species Classifier
def exercise1(SepalLen,SepalWid,PetalLen,PetalWid):
    FLOWERS = {"SETOSA":"setosa", "VERSICOLOR":"versicolor", "VIRGINCA":"virginica"}
    if PetalLen < 2.5: return FLOWERS["SETOSA"]
    if PetalWid < 1.8: 
        if PetalLen < 5:
            if PetalWid < 1.7: return FLOWERS["VERSICOLOR"]
            return FLOWERS["VIRGINCA"]
        if PetalWid < 1.6: return FLOWERS["VIRGINCA"]
        if SepalLen < 7: return FLOWERS["VERSICOLOR"]
        return FLOWERS["VIRGINCA"]
    if PetalLen >= 4.9: return FLOWERS["VIRGINCA"]
    if SepalLen < 6: return FLOWERS["VERSICOLOR"]
    return FLOWERS["VIRGINCA"]

# Exercise 2 - Dog Breeds Standards
def exercise2(breed,height,weight,male):
    STANDARD = {"Bulldog": { 1: { "h": 15, "w": 50 }, 0: { "h": 14, "w": 14 } }, "Dalmatian": { 1: { "h": 24, "w": 70 }, 0: { "h": 19, "w": 45 } }, "Maltese": { 1: { "h": 9, "w": 7 }, 0: { "h": 7, "w": 6 } }}
    std_h, std_w = STANDARD[breed][male]["h"], STANDARD[breed][male]["w"] # get the standards from the standard obj
    if std_h*0.9 <= height <= std_h*1.1 and std_w*0.9 <= weight <= std_w*1.1: return True
    return False

# Exercise 3 - Basic Statistics
def exercise3(l):
    def cal_stat(nums):
        half_idx = int(len(nums)/2)
        median = nums[half_idx] if len(nums) % 2 else (nums[half_idx]+nums[half_idx-1]) / 2
        return [min(nums), sum(nums)/len(nums), median, max(nums)]
    l.sort()
    return [tuple(cal_stat(l)), tuple(cal_stat([int(i**2) for i in l]))]

# Exercise 4 - Finite-State Machine Simulator
def exercise4(trans,init_state,input_list):
    output = []
    for input in input_list:
        result = trans[init_state + "/" + input].split("/")
        init_state = result[0] # update the state
        output.append(result[1]) # push the output to the output array
    return output

# Exercise 5 - Document Stats
def exercise5(filename):
    is_number = lambda char: (48 <= ord(char) <= 57)
    is_letter = lambda char: (65 <= ord(char) <= 90 or 97 <= ord(char) <= 122)
    is_endline = lambda char: (ord(char) in (10, 13))
    count = {"letters": 0, "numbers":0, "symbols": 0, "words": 0, "sentences": 0, "paragraphs": 0, "last_line_len": 0, "last_symbols":False}
    for line in open(filename, mode="r", encoding="utf-8").readlines(): # loop through each line
        if len(line) > 1 : # only doing operations when line is not empty
            if (count["last_line_len"] <= 1): count["paragraphs"] += 1 # count the paragraph when last line is empty and current line is not
            for word in line.split(" "): # splitting as word list by spaces
                if not (len(word) == 1 and not (is_letter(word[0]) or is_number(word[0]))): count["words"], count["last_symbols"] = count["words"]+1, False # eg. "-" not counted as word
                for idx, char in enumerate(word): # loop through each characters of the word with index
                    if char in (".", "?", "!"): count["sentences"] += 1 # symbols of ending a sentence
                    if is_number(char): 
                        count["numbers"] += 1
                        if count["last_symbols"]: count["words"], count["last_symbols"] = count["words"] + 1, False # adding word count for sub-words eg. 7-seas
                    elif is_letter(char):
                        count["letters"] += 1
                        if count["last_symbols"]: count["words"], count["last_symbols"] = count["words"] + 1, False # adding word count for sub-words eg. C-3PO
                    elif not is_endline(char): # exclude Line Feed \n & Carriage Return \r
                        count["symbols"] += 1
                        if not idx==0: count["last_symbols"] = True # ensure the symbol is in the middle of the word
        count["last_line_len"] = len(line) # record the length of this line
    return tuple([count["letters"], count["numbers"], count["symbols"], count["words"], count["sentences"], count["paragraphs"]])

# Exercise 6 - List Depth
def exercise6(l):
    max_depth = 0
    for e in l:
        if type(e) is list: # check if element is a sub-list
            depth = exercise6(e) # find the max depth of sub-list
            if depth > max_depth: max_depth = depth # compare with origin max depth
    return max_depth + 1

def exercise7(amount,coins):
    COINS = (2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01)
    for coin in COINS:
        if coins == 2: # only two coins left
            if amount - coin in COINS: return True
        else:  # more than two coins left
            if exercise7(amount - coin, coins - 1): return True
    return False

# Exercise 8 - Five Letter Unscramble
def exercise8(s):
    WORDS =  open("test_data/wordle.txt", mode="r", encoding="utf-8").readlines()
    def is_included(word, counts): # check if word can be scrambled using char appearence counts object of target word
        temp = copy.deepcopy(counts)
        for char in word: # loop through word being checked
            if not (char in temp): return False
            elif not temp[char] > 0: return False
            temp[char] -= 1 # decrease the appearence count of that char by 1
        return True
    s_counts, count = dict(), 0 # object for characters apearing counts of s and number count
    for char in s: s_counts[char] = s_counts[char]+1 if char in s_counts else 1
    for word in WORDS: # loop through each word to check if it is scramble
        if is_included(word.strip(), s_counts): count += 1
    return count

# Exercise 9 - Wordle Set
def exercise9(green,yellow,gray):
    words = open("test_data/wordle.txt", mode="r", encoding="utf-8").read().splitlines()
    for char in gray: words = list(filter(lambda word: not char in word, words))
    for char in yellow:
        for idx in yellow[char]: words = list(filter(lambda word: not (word[idx] == char) and (char in word), words))
    for idx in green: words = list(filter(lambda word: word[idx] == green[idx], words))
    return len(words)

# Exercise 10 - One Step of Wordle
def exercise10(green,yellow,gray):
    def cal_wordle_set(words, green, yellow, gray):
        for char in gray: words = list(filter(lambda word: not char in word, words))
        for char in yellow:
            for idx in yellow[char]: words = list(filter(lambda word: not (word[idx] == char) and (char in word), words))
        for idx in green: words = list(filter(lambda word: word[idx] == green[idx], words))
        return words
    first_set = open("test_data/wordle.txt", mode="r", encoding="utf-8").readlines() # first filtered wordle word set
    first_set = cal_wordle_set(first_set, green, yellow, gray)
    updated_config = word_scores = dict()
    lowest_scores = 999999999 
    for target_word_idx, target_word in enumerate(first_set): # loop through all the words to calculate scores
        scores = 0
        for other_word_idx, other_word in enumerate(first_set): # loop through the other words
            if (other_word_idx != target_word_idx): # not the target word which is to be calculated for scores
                updated_config = {"green":{}, "yellow": {}, "gray": set()}
                for letter_idx, letter in enumerate(target_word): # loop through ebvery letter of the target word
                    if letter == other_word[letter_idx]: updated_config["green"][letter_idx] = letter # check hypothetical correct letter
                    elif letter in other_word: updated_config["yellow"].setdefault(letter, []).append(letter_idx) # check hypothetical included letter
                    elif not letter in other_word: updated_config["gray"].add(letter) #  check hypothetical non-exist letter
                second_set = cal_wordle_set(first_set, updated_config["green"], updated_config["yellow"], updated_config["gray"])
                scores += len(second_set)
        if scores < lowest_scores: lowest_scores = scores
        word_scores.setdefault(scores, []).append(target_word.strip())
    return set(word_scores[lowest_scores])

