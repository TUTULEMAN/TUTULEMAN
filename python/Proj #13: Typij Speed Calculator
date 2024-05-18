import time

def createbox():
    border = '-*-'*10
    print(border)
    print()
    print('Try to enter this phrase as fast as possible')
    print()

def get_accuracy(input_text, original_text):
    input_words = input_text.split()
    original_words = original_text.split()
    return sum(1 for iw, ow in zip(input_words, original_words) if iw == ow) / len(original_words)

def typing_game():
    string = "This is a game made by Tuong Max Le, hope you enjoy"
    createbox()
    print(string, "\n")
    while True:
        t0 = time.time()
        input_text = str(input())
        t1 = time.time()
        length_of_input = len(input_text.split())
        accuracy = get_accuracy(input_text, string)
        time_taken = (t1-t0)
        words_per_minute = (length_of_input/time_taken)*60

        # show results
        print('Total words \t:', length_of_input)
        print('Time used \t:', round(time_taken,2), 'seconds')
        print('Accuracy \t:', round(accuracy,3)*100, '%')
        print('Speed is \t:', round(words_per_minute,2), 'words per minute')
        print('Do you want to retry? (yes/no)', end=' ')
        if input().lower() not in ['yes', 'y']:
            print('Thanks, good bye.')
            time.sleep(2)
            break
typing_game()

