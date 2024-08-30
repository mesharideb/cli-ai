import os
from openai import OpenAI
from colorama import Fore, Style, init
from dotenv import load_dotenv  
import sys
import random

# Initi colorama for colored output
init(autoreset=True)

# Load env variables from .env file
load_dotenv()

# Get the API key from the env variables
api_key = os.getenv('OPENAI_API_KEY')

# Create the OpenAI client
client = OpenAI(api_key=api_key)

# Responses for AI while doing his job (thinking)? 
thinking_responses = [
    "I am thinking... or maybe I'm just daydreaming!",
    "Give me a sec, my brain cells are on it!",
    "Calculating... or pretending to be a genius!",
    "Just a moment, my circuits are aligning.",
]

def chat_completion(input_text, model):
    """
    Function to interact with the OpenAI model and get the response.
    """
    try:
        # Display the thinking message while AI is processing
        print(Fore.CYAN + random.choice(thinking_responses) + Style.RESET_ALL)

        # Request a chat completion from the OpenAI API
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": input_text}],
            model=model,
            stream=True
        )

        # Display the response in chunks 
        full_response = ""
        for chunk in chat_completion:
            chunk_message = getattr(chunk.choices[0].delta, 'content', '')
            if chunk_message:
                full_response += chunk_message
                print(Fore.YELLOW + chunk_message + Style.RESET_ALL, end='', flush=True)
        print()  # Print a newline after the response is complete
        return full_response
    except Exception as e:
        # Handle exceptions 
        print(Fore.RED + f"Error: {str(e)}" + Style.RESET_ALL)
        return "An error occurred. Please try again."

def choose_model():
    """
    Function to allow the user to choose the OpenAI model.
    """
    available_models = ["gpt-3.5-turbo", "gpt-4", "gpt-3.5-turbo-16k"]
    print(Fore.GREEN + "Please choose a model for the chat session:" + Style.RESET_ALL)
    for i, model in enumerate(available_models, 1):
        print(Fore.CYAN + f"{i}. {model}" + Style.RESET_ALL)
    
    while True:
        try:
            choice = int(input(Fore.BLUE + "Enter the number of your choice: " + Style.RESET_ALL))
            if 1 <= choice <= len(available_models):
                return available_models[choice - 1]
            else:
                print(Fore.RED + "Invalid choice. Please select a valid model number." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Please enter a number." + Style.RESET_ALL)

def interactive_chat():
    """
    Function to start an interactive chat session with the OpenAI model.
    """
    print(Fore.GREEN + "Welcome to the interactive AI chat! Feel free to ask me anything." + Style.RESET_ALL)
    print(Fore.GREEN + "Type 'exit' or 'quit' to end the chat." + Style.RESET_ALL)

    # Let user choose the model
    model = choose_model()
    print(Fore.GREEN + f"Using model: {model}" + Style.RESET_ALL)
    print(Fore.GREEN + "Let's get started!" + Style.RESET_ALL)

    while True:
        user_input = input(Fore.BLUE + "You: " + Style.RESET_ALL)
        
        # Exit conditions
        if user_input.lower() in ['exit', 'quit']:
            print(Fore.GREEN + "It was fun! I’ll be here waiting… in the dark… no pressure. Goodbye!" + Style.RESET_ALL)
            break
        
        # Check for empty input
        if not user_input.strip():
            print(Fore.RED + "Silent treatment, huh? Well, I’m always here… waiting… in the silence. Care to break it with a question?" + Style.RESET_ALL)
            continue
        
        # Displaying AI's response
        print(Fore.YELLOW + "AI: " + Style.RESET_ALL, end='', flush=True)
        response = chat_completion(user_input, model)

# Start the interactive chat session
if __name__ == "__main__":
    try:
        interactive_chat()
    except KeyboardInterrupt:
        print(Fore.RED + "\nChat interrupted. Exiting... Hope to chat again soon!" + Style.RESET_ALL)
        sys.exit()