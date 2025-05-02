from spellchecker import SpellChecker

# Initialize the spellchecker
spell = SpellChecker()

# Read permutations from the file
with open("permutated_words.txt", "r") as file:
    permutations = file.read().splitlines()

# Check which words are valid
valid_words = [word for word in permutations if word in spell]

# Write valid words to a new file
# with open("valid_words.txt", "w") as output_file:
#    for word in valid_words:
#        output_file.write(word + "\n")
for word in valid_words:
    print(word)