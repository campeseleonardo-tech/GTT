# run_game.py
from app_ui import print_header, start_game

def main():
    print_header()
    s = input("Press Enter to Start (default 10 rounds) or type number of rounds: ").strip()
    try:
        rounds = int(s) if s else 10
    except:
        rounds = 10
    start_game(rounds)

if __name__ == "__main__":
    main()