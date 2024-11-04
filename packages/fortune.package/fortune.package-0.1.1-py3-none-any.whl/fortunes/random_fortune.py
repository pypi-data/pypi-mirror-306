# random_fortune.py
"""
this function will return you a random fortune cookie quote and a random lucky number
have fun!
"""

import random
import importlib.resources

def get_fortune_cookie():
    # Load the quotes from the fortune.txt file using importlib.resources
    with importlib.resources.open_text('fortunes', 'fortune.txt') as file:
        content = file.read()
        fortunes = [quote.strip() for quote in content.split('%') if quote.strip()]

    fortune = random.choice(fortunes)
    lucky_num = random.randint(0, 99)
    
    # Return the formatted fortune and lucky number
    return f"🔮 Your Fortune: {fortune}\n🍀 Your Lucky Number: {lucky_num}"
