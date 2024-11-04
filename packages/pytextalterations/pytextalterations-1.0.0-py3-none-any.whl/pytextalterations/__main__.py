import capitalize_sentences
import most_frequent_words
import remove
import sentence_count


def main():
    print('Welcome to Text Alterations')
    print('With this package you can: ')
    print('(C) Capitalize the first letter of sentences in a text')
    print('(F) List words in a text in order of frequency')
    print('(N) Find the number of sentences in a text')
    print('(R) Remove all the punctuation and capital letters in a text')

    option = find_input()

    while option != 'Quit':
        sentencestr = input("Please enter the text you want to alter: ")
        menu(option, sentencestr)
        option = find_input()



def find_input():
    option = input('Please choose an option (C, F, N, R, or Quit) to continue: ')
    while option != 'C' and option != 'F' and option != 'N' and option != 'R' and option != "Quit":
        option = input('Invalid! Please choose an option (C, F, N, R, or Quit) to continue: ')
    return option


def menu(option, sentencestr):
    if option == 'C':
        print('Here is the text with all sentences properly capitalized.')
        print(capitalize_sentences.capitalize_sentences(sentencestr))

    if option == 'F':
        print('Here are the words listed in order of frequency')
        print(most_frequent_words.most_frequent_words(sentencestr))

    if option == 'N':
        print('Here are the number of sentences: ', sentence_count.sentence_count(sentencestr))

    if option == 'R':
        print('Here is the text in lowercase with the punctuation removed.')
        print(remove.removepunctuation(sentencestr))



main()
print('Goodbye!')