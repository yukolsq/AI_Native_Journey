# Define the special name you want to check for
# Remember to replace "[Your Name]" with the actual name you want to use, e.g., "Alice" or "John"
SPECIAL_NAME = "Yuko" 

# Ask the user for their name and store it in the 'name' variable
name = input("What's your name? ") 

# You can keep the 'goal' fixed or also make it ask for input
goal = "AI Native builder"

# Now, use an if/else statement to check the name
if name == SPECIAL_NAME:
    # Special welcome message for the designated name
    print(f"Hey, it's the awesome AI Director, {name}!")
else:
    # Regular greeting for any other name
    print(f"Hello, my name is {name}. I'm learning AI to become an awesome {goal}.")
