# BohanCompliment

A fun Python package that generates random compliments to brighten your day.

## Table of Contents

- [Description](#description)
- [PyPI Page](#pypi-page)
- [Installation](#installation)
- [Virtual Environment & Dependencies](#virtual-environment--dependencies)
- [Running BohanCompliment](#running-bohancompliment)
- [Examples](#examples)
- [Contributing](#contributing)
- [Author](#author)

## Description

**BohanCompliment** is a Python package designed to generate random compliments. Whether you need a quick boost or want to share kind words with friends and colleagues, BohanCompliment provides a variety of functions to suit your needs. With support for multiple languages and personalized messages, it's a versatile tool for spreading positivity.

## PyPI Page

You can find **BohanCompliment** on PyPI [HERE](https://pypi.org/project/BohanCompliment/).

## Installation

Install **BohanCompliment** with pip:

```bash
pip install BohanCompliment
```

## Virtual Environment & Dependencies

Setting up the virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running BohanCompliment

After installation, BohanCompliment can be directly ran in Python scripts or interactivelty via the Python shell. Import the ComplimentGenerator class and create an instance:
```
from BohanCompliment import ComplimentGenerator

generator = ComplimentGenerator()
```


## Examples

### Function Parameters
1. compliment(name: str)
2. personalized_compliment(name: str, trait: str)
3. multi_compliment(name: str, count: int)
4. compliment_in_language(name: str, language: str)
5. add_compliment(compliment: str)
6. add_translation(language: str, compliments: List[str])
7. list_languages()

### Available Functions: 
compliment(name): Returns a random compliment for the given name:
```
from BohanCompliment import compliment
print(compliment("Alice"))

# Output: You're an awesome person, Alice!
```

personalized_compliment(name, trait): Returns a compliment focusing on a specific trait: 
```
from BohanCompliment import personalized_compliment
print(personalized_compliment("Bob", "sense of humor"))

# Output: Bob, your sense of humor is truly remarkable!
```

multi_compliment(name, count): Returns multiple compliments
```
from BohanCompliment import multi_compliment
compliments = multi_compliment("Charlie", 3)
for c in compliments:
    print(c)

# Output:
# You're a fantastic problem solver, Charlie!
# You have a great sense of humor, Charlie!
# Charlie, your code is so elegant!
```

compliment_in_language(name, language): Returns a compliment in a specific language ('en', 'es', 'fr')
```
from BohanCompliment import compliment_in_language
print(compliment_in_language("Dana", "es"))

# Output: ¡Eres increíble, Dana!

print(compliment_in_language("Eve", "de"))

# Output: Language 'de' not supported.
```

add_compliment(compliment: str): Adds a new compliment to the generator
```
from BohanCompliment import ComplimentGenerator

generator = ComplimentGenerator()
generator.add_compliment("{name}, your dedication to learning is inspiring!")
print(generator.compliment("Frank"))

# Possible Output: Frank, your dedication to learning is inspiring!
```

add_translation(language: str, compliments: List[str]): Adds compliments in a new language
```
from BohanCompliment import ComplimentGenerator

generator = ComplimentGenerator()
italian_compliments = [
    "Sei fantastico, {name}!",
    "{name}, il tuo lavoro è eccezionale!"
]
generator.add_translation("it", italian_compliments)
print(generator.compliment_in_language("Giulia", "it"))

# Output: Sei fantastico, Giulia!
```

list_languages(): Lists all supported languages
```
from BohanCompliment import ComplimentGenerator

generator = ComplimentGenerator()
print(generator.list_languages())

# Output: ['en', 'es', 'fr', 'de', 'it']
```



## Contributing
To contribute to this project, here are the following steps:

Clone the GitHub repository
```
git clone https://github.com/software-students-fall2024/3-python-package-bowohan.git
cd BohanCompliment
```

Set up and activate the virtual environment
```
python -m venv venv
source venve/bin/activate
```

Install the required dependencies

```
pip install -r requirements.txt
```

Build and test the python package
```
python -m build
pytest
```

## Author
Bohan Hou