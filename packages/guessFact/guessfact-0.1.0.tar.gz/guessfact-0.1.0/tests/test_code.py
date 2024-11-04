import pytest
from src.guessFact.code import (
    main_function,
    category_choice_validation,
    fact_choice_validation,
    coffee,
    music,
    food)

#Test for main_function
def test_main_function_case1(monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture) -> None:
    inputs = iter(["1","1","1"])
    monkeypatch.setattr("builtins.input",lambda _: next(inputs))
    main_function()
    captured = capfd.readouterr()
    expected_output_segments = [
        "Welcome to the Guess the Fact Game!",
        "In this game, you'll be presented with two statements about a chosen topic.",
        "Your task is to guess which statement is true.",
        "Let's get started",
        "Please choose a category:",
        "1: Music",
        "2: Coffee",
        "3: Food",
        "Please choose a sub-category:",
        "1: Classical",
        "2: Jazz",
        "3: Pop"
    ]
    output = captured.out
    for segment in expected_output_segments:
        assert segment in output

def test_main_function_case2(monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture) -> None:
    inputs = iter(["4","1","a","1","1"])
    monkeypatch.setattr("builtins.input",lambda _: next(inputs))
    main_function()
    captured = capfd.readouterr()
    expected_output_segments = [
        "Welcome to the Guess the Fact Game!",
        "In this game, you'll be presented with two statements about a chosen topic.",
        "Your task is to guess which statement is true.",
        "Let's get started",
        "Please choose a category:",
        "1: Music",
        "2: Coffee",
        "3: Food",
        "Please choose a sub-category:",
        "1: Classical",
        "2: Jazz",
        "3: Pop"
    ]
    output = captured.out
    for segment in expected_output_segments:
        assert segment in output

def test_main_function_case3(monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture) -> None:
    inputs = iter(["1","3","1"])
    monkeypatch.setattr("builtins.input",lambda _: next(inputs))
    main_function()
    captured = capfd.readouterr()
    expected_output_segments = [
        "Welcome to the Guess the Fact Game!",
        "In this game, you'll be presented with two statements about a chosen topic.",
        "Your task is to guess which statement is true.",
        "Let's get started",
        "Please choose a category:",
        "1: Music",
        "2: Coffee",
        "3: Food",
        "Please choose a sub-category:",
        "1: Classical",
        "2: Jazz",
        "3: Pop"
    ]
    output = captured.out
    for segment in expected_output_segments:
        assert segment in output

def test_main_function_case4(monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture) -> None:
    inputs = iter(["2","1","1"])
    monkeypatch.setattr("builtins.input",lambda _: next(inputs))
    main_function()
    captured = capfd.readouterr()
    expected_output_segments = [
        "Welcome to the Guess the Fact Game!",
        "In this game, you'll be presented with two statements about a chosen topic.",
        "Your task is to guess which statement is true.",
        "Let's get started",
        "Please choose a category:",
        "1: Music",
        "2: Coffee",
        "3: Food",
        "Please choose a sub-category:",
        "1: Historical Tales",
        "2: Coffee Culture",
        "3: Scientific Facts"
    ]
    output = captured.out
    for segment in expected_output_segments:
        assert segment in output
        
def test_main_function_case5(monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture) -> None:
    inputs = iter(["3","1","1"])
    monkeypatch.setattr("builtins.input",lambda _: next(inputs))
    main_function()
    captured = capfd.readouterr()
    expected_output_segments = [
        "Welcome to the Guess the Fact Game!",
        "In this game, you'll be presented with two statements about a chosen topic.",
        "Your task is to guess which statement is true.",
        "Let's get started",
        "Please choose a category:",
        "1: Music",
        "2: Coffee",
        "3: Food",
        "Please choose a sub-category:",
        "1: Desserts",
        "2: International Cuisines",
        "3: Street Food"
    ]
    output = captured.out
    for segment in expected_output_segments:
        assert segment in output

#Test for fact_choice_validation function
def test_fact_choice_validation_case1() -> None:
    assert fact_choice_validation("1") == True

def test_fact_choice_validation_case2() -> None:
    assert fact_choice_validation("2") == True
    
def test_fact_choice_validation_case3() -> None:
    assert fact_choice_validation(" 2") == False
    
def test_fact_choice_validation_case4() -> None:
    assert fact_choice_validation(" ") == False

def test_fact_choice_validation_case5() -> None:
    assert fact_choice_validation("3") == False

#Test for category_choice_validation function
def test_category_choice_validation_case1() -> None:
    assert category_choice_validation("1") == True

def test_category_choice_validation_case2() -> None:
    assert category_choice_validation("2") == True
    
def test_category_choice_validation_case3() -> None:
    assert category_choice_validation("3") == True

def test_category_choice_validation_case4() -> None:
    assert category_choice_validation("") == False
    
def test_category_choice_validation_case5() -> None:
    assert category_choice_validation("1") == True
    
def test_category_choice_validation_case6() -> None:
    assert category_choice_validation("4") == False


#test out put fact sub cat1
def test_coffee_valid_output_choices1( monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture):#

    sub_choice = 1

    # Mock user input to be "1"

    monkeypatch.setattr("builtins.input", lambda _: "1")
    coffee(sub_choice)

    # Capture printed output
    out = capfd.readouterr().out

    possible_outputs = [
        "1.According to legend, coffee was discovered when a goat herder noticed his 'goats' energy after eating coffee berries"\
            "\n2.In 15th-century Yemen, coffee beans were so valuable that merchants would trade them for gemstones", 

            "1.In medieval Ethiopia, coffee was once taxed under a 'wakefulness tax'"\
            "\n2.The Arabic root word for coffe -- qahwa -- originally refered to a type of wine"
    ]

    assert any(possible_output in out for possible_output in possible_outputs)

#test out put fact sub cat2
def test_coffee_valid_output_choices2( monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture):#

    sub_choice = 2

    # Mock user input to be "1"

    monkeypatch.setattr("builtins.input", lambda _: "1")
    coffee(sub_choice)

    # Capture printed output
    out = capfd.readouterr().out

    possible_outputs = [
        "1.According to global trade data, coffee is indeed one of the most traded commodities, second only to oil”\
            \n2.In a remote mountain village in Nepal, monks practice “coffee meditation", 
            
        "1.Finland consistently ranks first in coffee consumption per capita"\
        "\n2.In a small town in France, it’s customary to clink coffee mugs before every sip. Local folklore says it helps people “toast” the spirit of the coffee bean for good energy" 
            
    ]

    assert any(possible_output in out for possible_output in possible_outputs)

#test out put fact sub cat1 & unvalid input
def test_coffee_valid_output_choices3( monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture):#

    sub_choice = 3

    # Mock user input to be "3"then"1"
    inputs = iter(["a","4", "1"])
    monkeypatch.setattr("builtins.input",lambda _: next(inputs))
   # monkeypatch.setattr("builtins.input", lambda _: "1")
    coffee(sub_choice)

    # Capture printed output
    out = capfd.readouterr().out

    possible_outputs = [
       "1.In the highlands of Peru, there is a rare coffee plant that only blooms at midnight on full moons, releasing an unusually sweet aroma. The coffee from these “Lunar Beans” is said to have a mellow, caramel flavor"\
            "\n2.Coffee is one of the richest sources of antioxidants in the average diet, even more than some fruits and vegetables", 
            
        "1.Studies have found that just holding a warm cup of coffee can affect your perception and behavior."\
        "\n2.In a lab experiment, researchers in Iceland developed coffee beans that change color according to the drinker’s mood. These “Mood Beans” are still in development but are said to go from green (calm) to red (excited) as you take a sip"
            
    ]

    assert any(possible_output in out for possible_output in possible_outputs)

#test result sub cat1
def test_coffee_valid_result1( monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture):#

    sub_choice = 1

    # Mock user input to be "3"then"1"
    monkeypatch.setattr("builtins.input",lambda _: "1")

    coffee(sub_choice)

    # Capture printed output
    out = capfd.readouterr().out


    output1 = "1.According to legend, coffee was discovered when a goat herder noticed his 'goats' energy after eating coffee berries"\
            "\n2.In 15th-century Yemen, coffee beans were so valuable that merchants would trade them for gemstones"
    
    if output1 in out:
        assert "You are right," in out
    else:
        assert "You are wrong," in out

#test result sub cat2
def test_coffee_valid_result2( monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture):#

    sub_choice = 2

    # Mock user input to be "3"then"1"
    monkeypatch.setattr("builtins.input",lambda _: "1")

    coffee(sub_choice)

    # Capture printed output
    out = capfd.readouterr().out

    output1 = "1.According to global trade data, coffee is indeed one of the most traded commodities, second only to oil”\
            \n2.In a remote mountain village in Nepal, monks practice “coffee meditation"
    
    if output1 in out:
        assert "You are right," in out
    else:
        assert "You are right," in out

#test result sub cat3
def test_coffee_valid_result3( monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture):#

    sub_choice = 3

    # Mock user input to be "3"then"1"
    monkeypatch.setattr("builtins.input",lambda _: "1")

    coffee(sub_choice)

    # Capture printed output
    out = capfd.readouterr().out


    output1 = "1.In the highlands of Peru, there is a rare coffee plant that only blooms at midnight on full moons, releasing an unusually sweet aroma. The coffee from these “Lunar Beans” is said to have a mellow, caramel flavor"\
            "\n2.Coffee is one of the richest sources of antioxidants in the average diet, even more than some fruits and vegetables"
    
    if output1 in out:
        assert "You are wrong," in out
    else:
        assert "You are right," in out


# Test for Food function output and choices
def test_food_valid_output_choices1(monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture):
    sub_choice = 1
    monkeypatch.setattr("builtins.input", lambda _: "1")
    food(sub_choice)
    out = capfd.readouterr().out

    possible_outputs = [
        "1. The French dessert 'Mille-Feuille' is known for its hundreds of layers of thin pastry and cream."\
        "\n2. The original 'Mille-Feuille' was made using rice paper instead of pastry.",
        
        "1. Sushi originally started as a preservation method for fish in ancient China."\
        "\n2. Sushi rolls were initially created as a quick snack for soldiers in medieval Japan."
    ]
    assert any(possible_output in out for possible_output in possible_outputs)

def test_Food_valid_output_choices2(monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture):
    sub_choice = 2
    monkeypatch.setattr("builtins.input", lambda _: "1")
    food(sub_choice)
    out = capfd.readouterr().out

    possible_outputs = [
        "1. Street food vendors in Bangkok were once forbidden to sell food during daylight hours to prevent congestion."\
        "\n2. Bangkok is known as the 'Street Food Capital' because it holds the world record for the highest number of street vendors per square mile.",
        
        "1. French macarons were actually created in Italy and brought to France by Catherine de' Medici."\
        "\n2. The original macarons were filled with custard, not ganache or buttercream."
    ]
    assert any(possible_output in out for possible_output in possible_outputs)

def test_food_valid_output_choices3(monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture):
    sub_choice = 3
    monkeypatch.setattr("builtins.input", lambda _: "1")
    food(sub_choice)
    out = capfd.readouterr().out

    possible_outputs = [
        "1. The first recipe for 'tacos' was published in a 19th-century cookbook in Spain."\
        "\n2. Tacos are considered to have originated from silver miners in 18th-century Mexico.",
        
        "1. Ice cream was once considered an expensive luxury reserved for royal families."\
        "\n2. The first recorded flavor of ice cream was pistachio, which originated in Persia."
    ]
    assert any(possible_output in out for possible_output in possible_outputs)

# Test for correct result output
def test_food_valid_result1(monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture):
    sub_choice = 1
    monkeypatch.setattr("builtins.input", lambda _: "1")
    food(sub_choice)
    out = capfd.readouterr().out

    if "You are right," in out:
        assert True
    elif "You are wrong," in out:
        assert True
    else:
        assert False, "The test failed because no valid result was found in the output."

def test_food_valid_result2(monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture):
    sub_choice = 2
    monkeypatch.setattr("builtins.input", lambda _: "1")
    food(sub_choice)
    out = capfd.readouterr().out

    if "You are right," in out:
        assert True
    elif "You are wrong," in out:
        assert True
    else:
        assert False, "The test failed because no valid result was found in the output."

def test_food_valid_result3(monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture):
    sub_choice = 3
    monkeypatch.setattr("builtins.input", lambda _: "1")
    food(sub_choice)
    out = capfd.readouterr().out

    if "You are right," in out:
        assert True
    elif "You are wrong," in out:
        assert True
    else:
        assert False, "The test failed because no valid result was found in the output."

def test_music_valid_result1( monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture):
    # input user choice
    monkeypatch.setattr("builtins.input",lambda _: "1")

    music(1)

    # compare output with expected result
    out = capfd.readouterr().out
    assert "You are right" in out

def test_music_valid_result2( monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture):
    # input user choice
    monkeypatch.setattr("builtins.input",lambda _: "1")

    music(2)

    # compare output with expected result
    out = capfd.readouterr().out
    output1 = "1. Louis Armstrong’s influential trumpet playing helped shape modern jazz."
    if output1 in out:
        assert "You are right" in out
    else:
        assert "You are wrong" in out

def test_music_valid_result3( monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture):
    # input user choice
    monkeypatch.setattr("builtins.input",lambda _: "1")

    music(3)

    # compare output with expected result
    out = capfd.readouterr().out
    output1 = "1. Michael Jackson’s album Thriller is the best-selling album of all time."
    if output1 in out:
        assert "You are right" in out
    else:
        assert "You are wrong" in out