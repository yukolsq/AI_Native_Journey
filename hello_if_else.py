def print_welcome_message():
    name = "Yuko"
    # Let's add a variable to simulate a condition
    is_learning_ai = True  # Set to True if Yuko is currently learning, False if already an AI Native builder

    if is_learning_ai:
        message = f"Hello my name is {name}. I'm learning AI to become an awesome AI Native builder."
    else:
        message = f"Hello my name is {name}. I have become an awesome AI Native builder!"
    
    print(message)

if __name__ == "__main__":
    print_welcome_message()