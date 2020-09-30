# word_count.py
# ===================================================
# Implement a word counter that counts the number of
# occurrences of all the words in a file. The word
# counter will return the top X words, as indicated
# by the user.
# ===================================================

import re
from hash_map import HashMap

"""
This is the regular expression used to capture words. It could probably be endlessly
tweaked to catch more words, but this provides a standard we can test against, so don't
modify it for your assignment submission.
"""
rgx = re.compile("(\w[\w']*\w|\w)")

def hash_function_2(key):
    """
    This is a hash function that can be used for the hashmap.
    """

    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    keys = set()

    ht = HashMap(2500,hash_function_2)

    # This block of code will read a file one word as a time and
    # put the word in `w`. It should be left as starter code.
    with open(source) as f:
        for line in f:
            words = rgx.findall(line)
            for w in words:
                # add the word to the set of keys
                w = w.lower()
                keys.add(w)
                if ht.contains_key(w):
                    # if the hashmap already contains the key, get its index
                    hashmap_index = ht.get_index(w)
                    # get the linked list at that index
                    linked_list = ht.get_chain(hashmap_index)
                    # get the head of that linked list
                    node = linked_list.get_head()
                    while node is not None:
                        if node.key == w:
                            cur_val = node.value
                            node.value = cur_val + 1
                        node = node.next


                else:
                    # if the hashmap doesn't contain the key, put it in
                    ht.put(w, 1)

    # create list for the tuples
    wordcount_tuples = []
    for key in keys:
        # loop through the keys from earlier, get associated value, and add the pair to the list
        wordcount_tuples.append(tuple((key, ht.get(key))))

    length = len(wordcount_tuples)
    for i in range(length):
        for n in range(0, (length-i-1)):
            # Sort the list of key value pairs
            if (wordcount_tuples[n][1]) < (wordcount_tuples[n + 1][1]):
                old = wordcount_tuples[n]
                wordcount_tuples[n] = wordcount_tuples[n+1]
                wordcount_tuples[n+1] = old
    return_list = []
    for i in range(number):
        # get a list of 0-[number] pairs to return
        return_list.append(wordcount_tuples[i])
    return return_list



'''

print(top_words("alice.txt",10))  # COMMENT THIS OUT WHEN SUBMITTING TO GRADESCOPE
print()
top_set = [None] * number

for key in keys:
    key_value = ht.get(key)
    for i in top_set:
        cur_i_key = top_set[i]
        if not cur_i_key:
            top_set[i] = key
        elif ht.get(top_set[i]) < key_value:
            cur_i_
'''
