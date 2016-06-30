# py_hockey
Python pynguin hockey(studying tasks)
Game is crossplatform, but command below are for linux. 
Todo: add windows manual

## Dependencies
To run this project you have to install:
+ python 2.7
+ [the pygame library](http://www.pygame.org/download.shtml)

To run test tasks:
+ python nose tests
+ [nose html output plugin](https://github.com/nose-devs/nose/tree/master/examples/html_plugin)

## To run the game
type 
`python main.py`

you can manage game over configs:
./game_config.xml
./first_team_config.xml
./second_team_config.xml

## To run tests
To run all tests type:
```
./run_tests.sh
```
or
```
nosetests --verbosity=2 --with-html-output ./test/single_pinguin_tests.py
```

Test results would be printed at `results.html`

## To run particular test with gui
type
```
python main.py -t <test name>
```
for example:
```
python main.py -t simple_test
```

By default all tests applying to logic `YouLogic` in a file `pattern.py`
To test in, set the `pattern.py` content equals to:
```python

class YourLogic:

    def move(self, board, gate, index, side, balls, your_team, enemy_team):
        return (-5, 0)
```
and run again:
```
python main.py -t simple_test
```

It is a logic of pinguin, which always moves left. It should pass the first test. 

To apply tests for your own logic, change file and logic name in the head of `./test_sets.py`
```python
#test_file_name = "pattern"
#test_logic_name = "YourLogic"

test_file_name = "Metida"
test_logic_name = "P1"
```


## Logic
Pinguin logic is a class, with a default initializer and a function `move(...args...)`
Like this:
```python

class YourLogic:

    def move(self, board, gate, index, side, balls, your_team, enemy_team):
        return (0, 0)
```

Function `move` consumes a current board state and should return a tuple of two float digits: speed by axis 'x' and 'y' correspondingly. 
The axis 'x' is directed from left to right, axis 'y' from __top__ to __bottom__. 
The absolute value of tuple values must not exceeded 10, otherwise it will be "cut". 

### Board state
todo...


