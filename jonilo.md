# Jonilo.py

Hi!

Jonilo is our implementations of the Ultimate tic tac toe AI. To run
it, make sure to run the referee first using the command:

````
python referee.py jonilo jonilo --time_limit 120
````

after that, you can run:

````
python jonilo.py
````

For the project structure, there's a main class that runs on loop
for a .go file. After finds the file, another methos is reponsible for
running min and max with util and eval funtions. The return of that
is written in the move_file