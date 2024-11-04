"""This file should contains the code that will be implemented"""

def main_function() -> None:
    """the main function to implement the interaction with the user"""
    print("Welcome to the Guess the Fact Game!")
    print("In this game, you'll be presented with two statements about a chosen topic.")
    print("Your task is to guess which statement is true.")
    print("Let's get started!")
    print("Please choose a category:")
    categories = {"1": "Music","2": "Coffee","3": "Food"}
    for key, value in categories.items():
        print(f"{key}: {value}")
    category_choice = input("Enter the number of your chosen category: ")
    while True:
        if category_choice_validation(category_choice):
            break
        category_choice = input("Please enter the number 1, 2, or 3 to choose the category").strip()
    print("Please choose a sub-category:")
    if category_choice=="1":
        sub_categories = {"1": "Classical","2": "Jazz","3": "Pop"}
        for key, value in sub_categories.items():
            print(f"{key}: {value}")
        sub_choice = input("Enter the number of your chosen sub-category: ")
        while True:
            if category_choice_validation(sub_choice):
                break
            sub_choice = input(
                "Please enter the number 1, 2, or 3 to choose the sub-category").strip()
        music(sub_choice)
    elif category_choice=="2":
        sub_categories = {"1": "Historical Tales","2": "Coffee Culture","3": "Scientific Facts"}
        for key, value in sub_categories.items():
            print(f"{key}: {value}")
        sub_choice = input("Enter the number of your chosen sub-category: ")
        while True:
            if category_choice_validation(sub_choice):
                break
            sub_choice = input(
                "Please enter the number 1, 2, or 3 to choose the sub-category").strip()
        coffee(sub_choice)
    else: # Food category
        sub_categories = {"1": "Desserts","2": "International Cuisines","3": "Street Food"}
        for key, value in sub_categories.items():
            print(f"{key}: {value}")
        sub_choice = input("Enter the number of your chosen sub-category: ")
        while True:
            if category_choice_validation(sub_choice):
                break
            sub_choice = input(
                "Please enter the number 1, 2, or 3 to choose the sub-category").strip()
        food(sub_choice)

def category_choice_validation(category_choice: str) -> bool:
    """the function the check whether the user enter a valid category choice: 
    true if valid, false otherwise"""
    return (category_choice in {"1","2","3"})

def music(sub_choice: int) -> None:
    """argument: sub_choice (int), which will be 1, 2, or 3
    
    the function should do the following:
    
    1. store the two groups of statements 
    (one fact & one fabrication + another fact & another fabrication) 
    and their corresponding explanations
    
    2. randomly print one group to user, which will be two statements
    
    3. prompt user to enter 1 or 2 to choose the fact
    
    4. use while loop and fact_choice_validation function below to prompt again 
    until the fact_choice is valid
    
    5. check whether the user's answer correct
    
    6. tell the user whether she/he is correct or not
    
    7. give a little bit explanation for both statements
    
    8. write >= 3 tests for this function in the test_code.py"""

    facts = {
        1: [
            "1. Beethoven continued to compose even after he lost his hearing.\n2. Wolfgang Amadeus Mozart wrote over 1,000 symphonies in his lifetime.",
            "1. Frédéric Chopin was known for his operas and symphonies.\n2. Johann Sebastian Bach had 20 children."
        ],
        2: [
            "1. Louis Armstrong’s influential trumpet playing helped shape modern jazz.\n2. Jazz originated in London during the 19th century.",
            "1. Duke Ellington was primarily known as a classical pianist and rarely performed jazz.\n2. Louis Armstrong, one of the most influential figures in jazz, was also known for his distinctive gravelly voice and popularized scat singing."
        ],
        3: [
            "1. Michael Jackson’s album Thriller is the best-selling album of all time.\n2. The Rolling Stones were originally known as The Blueberries.",
            "1. The Beatles were the first band to perform on the moon.\n2. The Beatles were originally known as The Quarrymen."
        ]
    }

    truths = {
        1: [ 1, 1 ],
        2: [ 1, 2 ],
        3: [ 1, 2 ]
    }

    explanations = {
        1: ["Beethoven composed the moonlight sonata after his loss of hearing.", "Chopin was known primarily for his piano compositions, not his symphony work."],
        2: ["Armstrongs influence on jazz extends even to today.", "Armstrongs distinctive singing captured the attention of audiences country wide."],
        3: ["Michael Jacksons album hit the best sellers list at the time.", "The beatles were not the first band to perform on the moon."]
    }

    sub_choice = int(sub_choice)
    
    statements = facts[sub_choice]
    statementIndex = int(__import__('time').time() * 1000) % 2
    selected_statement = statements[statementIndex]
    print(selected_statement)
    choice = input("Which fun fact do you think is true? Please type 1 or 2: ")
    while True:
        if fact_choice_validation(choice):
            break
        choice = input("Invalid input. Please enter either 1 or 2:")
    if int(choice) == truths[sub_choice][statementIndex]:
        print("You are right, "+explanations[sub_choice][statementIndex])
    else:
        print("You are wrong, "+explanations[sub_choice][statementIndex])

def coffee(sub_choice: int) -> None:

    #subcategories: 1.historical tales; 2.coffee culture; 3.scientific facts
    """
    1.1.
        1.According to legend, coffee was coffee was discovered when a goat herder noticed his goats’ energy after eating coffee berries
        2.In 15th-century Yemen, coffee beans were so valuable that merchants would trade them for gemstones.
    1.2
        1.In medieval Ethiopia, coffee was once taxed under a 'wakefulness tax'
        2.The Arabic root word for coffe -- qahwa -- originally refered to a type of wine
    2.1
        1.According to global trade data, coffee is indeed one of the most traded commodities, second only to oil
        2.2.In a remote mountain village in Nepal, monks practice “coffee meditation
    2.2
        1.Finland consistently ranks first in coffee consumption per capita
        2.In a small town in France, it’s customary to clink coffee mugs before every sip. Local folklore says it helps people “toast” the spirit of the coffee bean for good energy
    3.1
        1.In the highlands of Peru, there is a rare coffee plant that only blooms at midnight on full moons, releasing an unusually sweet aroma. The coffee from these “Lunar Beans” is said to have a mellow, caramel flavor
        2.Coffee is one of the richest sources of antioxidants in the average diet, even more than some fruits and vegetables
    3.2
        1.Studies have found that just holding a warm cup of coffee can affect your perception and behavior.
        2.In a lab experiment, researchers in Iceland developed coffee beans that change color according to the drinker’s mood. These “Mood Beans” are still in development but are said to go from green (calm) to red (excited) as you take a sip

    """

    facts = ["1.According to legend, coffee was discovered when a goat herder noticed his 'goats' energy after eating coffee berries"\
            "\n2.In 15th-century Yemen, coffee beans were so valuable that merchants would trade them for gemstones", 

            "1.In medieval Ethiopia, coffee was once taxed under a 'wakefulness tax'"\
            "\n2.The Arabic root word for coffe -- qahwa -- originally refered to a type of wine", 

            "1.According to global trade data, coffee is indeed one of the most traded commodities, second only to oil”\
            \n2.In a remote mountain village in Nepal, monks practice “coffee meditation", 
            
            "1.Finland consistently ranks first in coffee consumption per capita"\
            "\n2.In a small town in France, it’s customary to clink coffee mugs before every sip. Local folklore says it helps people “toast” the spirit of the coffee bean for good energy", 
            
            "1.In the highlands of Peru, there is a rare coffee plant that only blooms at midnight on full moons, releasing an unusually sweet aroma. The coffee from these “Lunar Beans” is said to have a mellow, caramel flavor"\
            "\n2.Coffee is one of the richest sources of antioxidants in the average diet, even more than some fruits and vegetables", 
            
            "1.Studies have found that just holding a warm cup of coffee can affect your perception and behavior."\
            "\n2.In a lab experiment, researchers in Iceland developed coffee beans that change color according to the drinker’s mood. These “Mood Beans” are still in development but are said to go from green (calm) to red (excited) as you take a sip"]
    
    explanation = ["choice 2 is made up. The legend in choice 1 comes from Ethiopia", 
                   "choice 1 is made up. As for choice 2, when coffee spread to Europe, it eventually morphed into caffè in Italian and coffee in English", 
                   "choice 2 is made up. Coffee is indeed the second traded commodities", 
                   "choice 2 is made up. Finland tops the list for coffee consumption per capita. On average, a Finnish person drinks nearly four cups a day!", 
                   "choice 1 is made up. Unfortunatly we don't mood beans in real world", 
                   "choice 2 is made up. People holding warm beverages often feel more positive toward others and even perceive the environment as warmer. This psychological effect, known as embodied cognition, links physical warmth with emotional warmth"]
    
    truth = [1, 2, 1, 1, 2, 1]
    
    #randomly generate 0 or 1
    random_value = int(__import__('time').time() * 1000) % 2

    sub_choice = int(sub_choice)
    #print facts
    print(facts[(sub_choice -1)*2+random_value])

    fact_choice = input("Which fun fact do you think is true? Please type 1 or 2: ")

    while True:
        if fact_choice_validation(fact_choice):
            break
        fact_choice = input("Invalid input. Please enter either 1 or 2:").strip()
    fact_choice = int(fact_choice)
    if fact_choice == truth[(sub_choice -1)*2+random_value]:
        print("You are right, "+explanation[(sub_choice -1)*2+random_value])
    else:
        print("You are wrong, "+explanation[(sub_choice -1)*2+random_value])

def food(sub_choice: int) -> None:

    facts = [
        "1. The French dessert 'Mille-Feuille' is known for its hundreds of layers of thin pastry and cream."\
        "\n2. The original 'Mille-Feuille' was made using rice paper instead of pastry.",
        
        "1. Sushi originally started as a preservation method for fish in ancient China."\
        "\n2. Sushi rolls were initially created as a quick snack for soldiers in medieval Japan.",
        
        "1. Street food vendors in Bangkok were once forbidden to sell food during daylight hours to prevent congestion."\
        "\n2. Bangkok is known as the 'Street Food Capital' because it holds the world record for the highest number of street vendors per square mile.",
        
        "1. French macarons were actually created in Italy and brought to France by Catherine de' Medici."\
        "\n2. The original macarons were filled with custard, not ganache or buttercream.",
        
        "1. The first recipe for 'tacos' was published in a 19th-century cookbook in Spain."\
        "\n2. Tacos are considered to have originated from silver miners in 18th-century Mexico.",
        
        "1. Ice cream was once considered an expensive luxury reserved for royal families."\
        "\n2. The first recorded flavor of ice cream was pistachio, which originated in Persia."
    ]

    explanation = [
        "Choice 2 is made up. Mille-Feuille has always been known for its thin pastry layers.",
        "Choice 2 is made up. Sushi indeed started as a preservation method, but the concept of rolls came much later.",
        "Choice 1 is made up. Bangkok is known for street food but there was no restriction based on daylight.",
        "Choice 2 is made up. Macarons were originally made with almonds and evolved into modern ganache filling.",
        "Choice 1 is made up. Tacos originated from Mexican miners.",
        "Choice 2 is made up. Early ice cream flavors were fruit-based, not pistachio."
    ]

    truth = [1, 1, 2, 1, 2, 1]
    random_value = int(__import__('time').time() * 1000) % 2
    sub_choice = int(sub_choice)

    print(facts[(sub_choice - 1) * 2 + random_value])

    fact_choice = input("Which fun fact do you think is true? Please type 1 or 2: ")

    while True:
        if fact_choice_validation(fact_choice):
            break
        fact_choice = input("Invalid input. Please enter either 1 or 2:").strip()

    fact_choice = int(fact_choice)

    if fact_choice == truth[(sub_choice - 1) * 2 + random_value]:
        print("You are right, " + explanation[(sub_choice - 1) * 2 + random_value])
    else:
        print("You are wrong, " + explanation[(sub_choice - 1) * 2 + random_value])

def fact_choice_validation(fact_choice: str) -> bool:
    """the function the check whether the user enter a valid fact choice: 
    true if valid, false otherwise"""
    return (fact_choice in {"1","2"})
