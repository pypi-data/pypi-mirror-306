# getMultipleFortunes.py
import random
import importlib.resources

def getMultipleFortunes(n):
    # Use importlib.resources to safely access the fortune.txt file
    with importlib.resources.open_text('fortunes', 'fortune.txt') as file:
        fortunes = [fortune.strip() for fortune in file.read().split('%') if fortune.strip()]
    if n > len(fortunes):
        raise ValueError("Requested more unique fortunes than available in fortune.txt")
    result = []
    for _ in range(n):
        num = random.randint(1, 100)
        fortune = random.choice(fortunes)
        while fortune in result:
            fortune = random.choice(fortunes)
        result.append(f"🔮 Your Fortune: {fortune}\n🍀 Your Lucky Number: {num}")
    
    return result

