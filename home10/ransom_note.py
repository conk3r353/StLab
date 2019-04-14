import collections

# Complete the checkMagazine function below.
def checkMagazine(magazine, note):
    magazine_dict = collections.Counter(magazine)
    note_dict = collections.Counter(note)
    magazine_dict.subtract(note_dict)

    for value in magazine_dict.values():
        if value < 0:
            return False
    return True