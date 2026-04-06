# Homework 3 - Board Game System
# Name:Carter Guthrie
# Date:4/5/2026

from graphics import *

# --- 1. FILE HANDLING FUNCTIONS ---

def load_game_state(filename):
    """Reads the game state from events.txt and returns a dictionary."""
    game_data = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                if ":" in line:
                    key, value = line.strip().split(":")
                    # Try to make the key (position) an integer
                    try:
                        game_data[int(key)] = value.strip()
                    except ValueError:
                        game_data[key.strip()] = value.strip()
        return game_data
    except FileNotFoundError:
        print("Error: events.txt not found.")
        return {"Turn": "Player1", 1: "Player1", 2: "Player2"}

def save_game_state(filename, game_data):
    """Writes the current dictionary back to events.txt."""
    with open(filename, 'w') as file:
        # Save Turn first
        file.write(f"Turn: {game_data.get('Turn', 'Player1')}\n")
        # Save positions/events
        for pos, entity in game_data.items():
            if pos != "Turn":
                file.write(f"{pos}: {entity}\n")

# --- 2. GAME LOGIC & DISPLAY FUNCTIONS ---

def draw_board(win, game_data):
    """Clears the window and draws the current state of the board."""
    # Clear existing items
    for item in win.items[:]:
        item.undraw()
    
    # Draw a simple horizontal board (Squares 1-10)
    for i in range(1, 11):
        square = Rectangle(Point(i*50 - 40, 100), Point(i*50 + 10, 150))
        square.draw(win)
        
        label = Text(Point(i*50 - 15, 165), str(i))
        label.draw(win)

        # Check if anything is at this position in our data
        if i in game_data:
            content = Text(Point(i*50 - 15, 125), game_data[i])
            content.setSize(8)
            content.draw(win)

    # Show current turn
    turn_text = Text(Point(250, 50), f"Current Turn: {game_data['Turn']}")
    turn_text.setStyle("bold")
    turn_text.draw(win)

def move_player(game_data, player_name, steps):
    """Finds the player, moves them, and handles turn switching."""
    old_pos = -1
    # Find current position
    for pos, entity in game_data.items():
        if entity == player_name:
            old_pos = pos
            break
    
    if old_pos != -1:
        new_pos = old_pos + steps
        # Basic boundary check (keep it on our 1-10 board for now)
        if new_pos > 10: new_pos = 10
        
        # Update Dictionary
        del game_data[old_pos]
        game_data[new_pos] = player_name
        
        # Switch Turn
        game_data["Turn"] = "Player2" if player_name == "Player1" else "Player1"
        return True
    return False

# --- 3. MAIN INTERACTION LOOP ---

def main():
    # Setup Window
    win = GraphWin("Homework 3 - Board Game", 600, 300)
    
    # Initial Load
    game_state = load_game_state("events.txt")
    
    while True:
        draw_board(win, game_state)
        
        # Interaction: Click or Press a key to move the current player
        print(f"It is {game_state['Turn']}'s turn. Click the window to roll and move!")
        win.getMouse() 
        
        # Logic: Move current player 1 step forward
        current_player = game_state["Turn"]
        move_player(game_state, current_player, 1)
        
        # Save progress
        save_game_state("events.txt", game_state)
        
        # Check if window is closed
        if win.isClosed():
            break

if __name__ == "__main__":
    main()