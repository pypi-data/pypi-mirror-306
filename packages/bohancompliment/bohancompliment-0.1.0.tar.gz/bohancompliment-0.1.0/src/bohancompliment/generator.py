# src/complimenter/generator.py

import random

compliments = [
    "You're an awesome person, {name}!",
    "{name}, your code is so elegant!",
    "You have a great sense of humor, {name}!",
    "{name}, your positivity is infectious!",
    "You're a fantastic problem solver, {name}!",
]

def compliment(name):
    """Generates a random compliment for the given name."""
    return random.choice(compliments).format(name=name)

def personalized_compliment(name, trait):
    """Generates a compliment focusing on a specific trait."""
    return f"{name}, your {trait} is truly remarkable!"

def multi_compliment(name, count):
    """Generates a specified number of compliments."""
    return [compliment(name) for _ in range(count)]

def compliment_in_language(name, language):
    """Generates a compliment in the specified language."""
    compliments_translations = {
        'en': f"You're amazing, {name}!",
        'es': f"¡Eres increíble, {name}!",
        'fr': f"Tu es incroyable, {name}!",
    }
    return compliments_translations.get(language, f"Language '{language}' not supported.")
