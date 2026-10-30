import os,random,json
from colorama import init, Fore, Back, Style
init(autoreset=True)
def main ():
    #goy
    with open("stats.JSON", "r") as f:
        stats = json.load(f)

    with open("word_list.txt", "r") as f:
        words = f.read().upper().splitlines()

    def save_stats(stats):
        with open("stats.JSON", "w") as f:
            json.dump(stats, f, indent=4)
    
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    def line():
            print(Style.BRIGHT+"--------------------")

    def initialize(words):
        words = list(set(words)-set(stats["past_words"]))
        random_word = random.choice(words)
        clear_screen()
        for i in range(6):
            print("[ ][ ][ ][ ][ ]")
        line()
        return random_word

    stats["Games_played"]+=1
    answer = initialize(words)
    stats["past_words"].append(answer)
    attempt = ["First","Second","Third","Fourth","Fifth","Final"]
    win = False
    count = 0
    guesses = []
   
    current_display = ["[ ][ ][ ][ ][ ]","[ ][ ][ ][ ][ ]","[ ][ ][ ][ ][ ]","[ ][ ][ ][ ][ ]","[ ][ ][ ][ ][ ]","[ ][ ][ ][ ][ ]"]

    def guess_check(guess,answer):
        display = []
        for i in range(5):
            if guess[i] == answer[i]:
                display.append(Back.GREEN+f"[{guess[i]}]")
            elif guess[i] in answer:
                display.append(Back.YELLOW+f"[{guess[i]}]")
            else:
                display.append(Back.RED+f"[{guess[i]}]")
        send = "".join(display)
        return send

    def play_again():
        again = input("Play again? ").lower()
        if again in ["yes","y",""]:
            main()

    def display_stats():
        wins = stats["Total_wins"]
        total_games = stats["Games_played"]
        line()
        print(Style.BRIGHT+"Stats")
        print(f"Total wins: {wins}")
        rate = (wins/total_games)*100
        print(f"Win rate: {rate:.0f}%")
        line()
        
    save = input("Do you want to save stats?: ").lower() in ["yes","y",""]
    while win or count<6:
        guess = input(f"{attempt[count]} guess: ").upper()
        while len(guess) != 5 or guess not in words:
            print("Try again. Guess must be a real 5-letter word.")
            guess = input(f"{attempt[count]} guess: ").upper()
        guesses.append(guess)
        current_display[count] = guess_check(guess,answer)
        clear_screen()
        print(*current_display, sep="\n")
        line()
        if guess == answer:
            print("You win!")
            print(f"The correct word was {answer.capitalize()}!")
            stats["Total_wins"] +=1
            if save:
                save_stats(stats)
                display_stats()
            play_again()
            count = 6
        elif count==5:
            print(f"You lost!\nThe word was {answer.capitalize()}.")
            stats["Total_losses"]+=1
            if save:
                save_stats(stats)
                display_stats()
            play_again()
            count+=1
        else:
            count +=1 
        
main()