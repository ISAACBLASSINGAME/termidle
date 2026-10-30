import os,random,json,statistics
from colorama import init, Fore, Back, Style
init(autoreset=True)
def main():
    save = input("Do you want to save stats?: ").lower() in ["yes","y",""]
    def game ():
        
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
                print(Style.BRIGHT+"-----------------------------------")

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
                game()

        def display_stats():
            wins = stats["Total_wins"]
            total_games = stats["Games_played"]
            average_guesses = statistics.mean(stats["number_of_guesses"])
            line()
            print(Style.BRIGHT+"Stats")
            print(f"Total wins: {wins}")
            rate = (wins/total_games)*100
            print(f"Win rate: {rate:.0f}%")
            print(f"Average guesses: {average_guesses:.2f}")
            line()
            
        
        while win or count<6:
            guess = input(f"{attempt[count]} guess: ").upper()
            while (len(guess) != 5 or guess not in words) and guess.lower() != "end":
                print("Try again. Guess must be a real 5-letter word.")
                guess = input(f"{attempt[count]} guess: ").upper()
            if guess.lower() != "end":
                guesses.append(guess)
                current_display[count] = guess_check(guess,answer)
                clear_screen()
                print(*current_display, sep="\n")
                line()
                if guess == answer:
                    print("You win!")
                    print(f"The correct word was {answer.capitalize()}!")
                    stats["Total_wins"] +=1
                    stats["number_of_guesses"].append(count+1)
                    if save:
                        save_stats(stats)
                        display_stats()
                    play_again()
                    count = 6
                elif count==5:
                    print(f"You lost!\nThe word was {answer.capitalize()}.")
                    stats["Total_losses"]+=1
                    stats["number_of_guesses"].append(6)
                    if save:
                        save_stats(stats)
                        display_stats()
                    play_again()
                    count+=1
                else:
                    count +=1 
            else:
                print(f"The word was {answer.capitalize()}.")
                print("Exiting game")
                if save:
                    stats["Total_losses"]+=1
                    save_stats(stats)
                count = 6
    game()
        
main()