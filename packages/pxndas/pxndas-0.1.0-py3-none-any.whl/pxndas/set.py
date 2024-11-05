ALLCHAR = set(input("Enter a set of characters: "))

VOWEL = set()
CONSONANTS = set()

for char in ALLCHAR:
    if char.lower() in 'aeiou':
        VOWEL.add(char)
    else:
        CONSONANTS.add(char)

NEW = {'C', 'O', 'M', 'P', 'U', 'T', 'E', 'R'}

print("The character in ALLCHAR : ",(ALLCHAR))
print("No.of element in ALLCHAR: ", len(ALLCHAR))
print("The vowel is: ", (VOWEL))
print("No.of element in VOWEL: ", len(VOWEL))
print("The consonants is: ",(CONSONANTS))
print("No.of element in CONSONANTS: ", len(CONSONANTS))

print("The character in NEW:", NEW)
print("No.of chracter in NEW :", len(NEW))
NEW.remove('R')
print("NEWCOPY after removing elements 'R': ", NEW)
print("After adding VOWEL and CONSONANTS: ", VOWEL.union(CONSONANTS))
print("Comman elements: ", NEW.intersection(CONSONANTS))
NEW.clear()
print("After deleting all the element: ", NEW)

del VOWEL
