def word_to_vector(word):
    # Define some basic rules for our vector components
    vector = [0] * 5  # Initialize a vector of 5 dimensions

    # Rule 1: Length of the word (normalized to a max of 10 characters for simplicity)
    vector[0] = len(word) / 10

    # Rule 2: Number of vowels in the word (normalized to the length of the word)
    vowels = "aeiou"
    vector[1] = sum(1 for char in word if char in vowels) / len(word)

    # Rule 3: Whether the word starts with a vowel (1) or not (0)
    vector[2] = 1 if word[0] in vowels else 0

    # Rule 4: Whether the word ends with a vowel (1) or not (0)
    vector[3] = 1 if word[-1] in vowels else 0

    # Rule 5: Percentage of consonants in the word
    vector[4] = sum(1 for char in word if char not in vowels and char.isalpha()) / len(
        word
    )

    return vector


# Example usage
word = "example"
vector = word_to_vector(word)
print(f"Word: {word}\nVector: {vector}")
