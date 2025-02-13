# Created by Ben Byerly
# Date: 2/11/2025
# The goal of this program is to solve the caesar cipher. It will take in an encrypted text and decrypt it. 
    # This program only works for the given cipher text below as per requested by the given assignment. 
    # It can be modified to work with any encrypted caesar cipher text in the future. 
    # not the neatest program but it works lol
# Commited to github 
"""
IT STY XYZRGQJ TAJW XTRJYMNSL GJMNSI DTZ  
"""
frequency_scale = { # frequency scale needed to be global didnt want to keep up with allat
    'A': 0.080, 'B': 0.015, 'C': 0.030, 'D': 0.040, 'E': 0.130,
    'F': 0.020, 'G': 0.015, 'H': 0.060, 'I': 0.065, 'J': 0.005,
    'K': 0.005, 'L': 0.035, 'M': 0.030, 'N': 0.070, 'O': 0.080,
    'P': 0.020, 'Q': 0.002, 'R': 0.065, 'S': 0.060, 'T': 0.090,
    'U': 0.030, 'V': 0.010, 'W': 0.015, 'X': 0.005, 'Y': 0.020,
    'Z': 0.015
}

def frequency_of_letters(cipher_text):
    # creates a dictionary 
    freq_dict={}
    # gets ride of spaces
    cipher_text_replace = cipher_text.replace(" ","")

    # initializes the dictionary with 0
    for i in cipher_text_replace:
        freq_dict[i] = 0         

    # counts the frequency of each letter      
    for i in cipher_text_replace:
        freq_dict[i] += 1

    print(f"\nTotal Numbers: {len(cipher_text_replace)}")
    print("Number of times each letter shows up in the cipher text: ")
    
    # i is the letter and count is how many times it shows up in the cipher text
    for i, count in freq_dict.items():   # iterates through the dictionary items
        print(f"{i}:{count}", end=" ")   # prints the frequency of each letter on one line

    return freq_dict, cipher_text_replace   # returns the dictionary and the cipher text without spaces


def character_frequency(freq_dict, cipher_text_replaced):
    # creates a dict for character freq 
    character_freq_dict = {}
    for i in freq_dict:                                      
        # calculates the character freq of each letter
        # takes the frequency of each letter that shows up in the cipher text and divides it by the total number of letters in the cipher text
        character_freq_dict[i] = freq_dict[i]/len(cipher_text_replaced) 
    print(f"\n\nCharacter Frequency: ")
    for i, count in character_freq_dict.items(): # iterates through the dictionary items
        print(f"{i}: {count:.4f}", end=" ")      # prints the character freq of each letter on one line to 4 decimal places
    print("\n")                                     # new line but for some reason print() didnt work
    return character_freq_dict


# holy shit i wanted to blow my brains out 
# this calculates the correlation of frequency between the english alphabet and the cipher text.
def correlation_of_frequency(character_freq_dict):
    correlations = {}                                      # creates a dictionary for the correlations
    for i in range(26):                                    # iterates 26 times for the alphabet
        correlation = 0                                    # initializes the correlation to 0 for each outer loop to reset

        for j, freq in character_freq_dict.items():     # iterates through the dictionary items

            if j in frequency_scale:                     # checks if the character is in the frequency scale which is always true 

                # had to look up how to change capital letters to their unicode values
                # this will get the position of each letter in the english alphabet
                # for exmample the function ord('A') - ord ('A') will return 0 which is the position of A in the alphabet
                # ord('B') - ord('A') will return 1 which is the position of B in the alphabet
                # j would be the 'A', 'B', 'C'...etc 
                alphabet_position = ord(j) - ord('A')

                # this is the (e – i) mod 26 part of the formula with the alphabet position calculated above
                shifted_position = (alphabet_position - i) % 26  

                # this will convert the shifted position back to a character
                shifted_char = chr(shifted_position + ord('A'))

                # this adds up all the correlations from the current loop so using example from class: .1 * (6 - i) + .1 * (7 - i) where e-i already calculated above
                # made this in parts because it was hard to mentally grasp
                correlation += freq * frequency_scale.get(shifted_char, 0)
        correlations[i] = correlation
    return correlations

def decryption(cipher_text, highest_correlation):

    decrypted_text = ""
    for i in cipher_text:
        if i.isalpha():  # will only shift characters that are alphanumeric this makes it easy to keep the spaces in the text
            # ord(i) ord('A') converts the letter into 0-25 range
            # - highest_correlation will shift the letter according to the maximum correlation
            # %26 allows to wrap around the alphabet
            # then + ord('A') converts the number back to to a letter
            decrypted_text += chr((ord(i) - ord('A') - highest_correlation) % 26 + ord('A'))
        else:
            decrypted_text += i # keeps spaces

    return decrypted_text


if __name__ == "__main__":
    # gets the cipher text from the user
    cipher_text = input("Input your cipher text: ")

    # gets the frequency of the letters in the cipher and the cipher text without spaces
    freq_dict, cipher_text_replace = frequency_of_letters(cipher_text.upper())

    # gets the character frequencies of all the letters in the cipher text    
    character_freq_dict = character_frequency(freq_dict, cipher_text_replace)

    # gets the correlation of the character frequency of the cipher text with the formula  f(c)f’(e – i) 
    # but modified a little bit using unicode equivalents of the alphabet by subtracting the unicode of 'A'. 
    correlations = correlation_of_frequency(character_freq_dict)

    # prints the correlations and its i value. 
    for shift, correlation in correlations.items():
        print(f"i = {shift}: {correlation:.4f}")

        # gets the i value with the highest correlation
        highest_correlation = max(correlations, key=correlations.get) # kept getting a TypeError when using max(correlations.values())
    # prints the highest correlation and the shift value
    print(f"\nHighest correlation of frequency is: {correlations[highest_correlation]:.4f}")
    print(f"The shift value is: {highest_correlation}")

    # calls decryption makes sures all values are upper and will pass the highest correlation
    decrypt_text = decryption(cipher_text.upper(), highest_correlation)
    print(f"\nThe decrypted text is: {decrypt_text}")
