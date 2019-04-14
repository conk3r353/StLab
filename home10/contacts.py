import collections


contacts = collections.Counter()


def word_split(word):
    return [word[0:i] for i in range(1, len(word) + 1)]


def add(word):
    for part in word_split(word):
        contacts[part] += 1


def find(word):
    return contacts.get(word, 0)