from time import sleep
from .pet import new_pet

def main():
    pet = new_pet()  

    try:
        while pet.stats["health"] > 0:
            
            pet.display_art()

            
            pet.status()

            
            command = input("\nEnter a command (e.g., 'feed 10', 'sleep 5', 'play 15', 'rename new_name', or 'leave'): ")
            parts = command.split(maxsplit=1)
            
            if len(parts) == 0:
                print("Invalid command.")
                continue

            action = parts[0].lower()

            
            if action == "feed" and len(parts) > 1 and parts[1].isdigit():
                pet.feed(int(parts[1]))
            elif action == "play" and len(parts) > 1 and parts[1].isdigit():
                pet.play(int(parts[1]))
            elif action == "sleep" and len(parts) > 1 and parts[1].isdigit():
                pet.sleep(int(parts[1]))
            elif action == "wait":
                print("You chose to wait...")
            elif action == "rename" and len(parts) > 1:
                pet.rename(parts[1])  
            elif action == "leave":
                print("You have chosen to leave the game.")
                break  
            else:
                print("Invalid command. Please use 'feed {amount}', 'play {duration}', 'sleep {duration}', 'rename {new_name}', 'wait', or 'leave'.")

            
            pet.update_stats()
            
            
            sleep(1)

    except KeyboardInterrupt:
        print("\nExiting the simulation.")
    
    print(f"\n{pet.name} has unfortunately reached zero health. Game over.")

if __name__ == "__main__":
    main()