# Lottery

Basic console program that has a lottery mechanism. It gives the possibility of adding a coupon and making a draw. Takes lottery details from file with json content.

# Technologies:

Python 3.5.2.
PostgreSQL
JSON

# Functions:

sql_execute - function responsible for connecting to database and executing given SQL command.

check_file - Asks for directory of file. Checks if the path is correct and whether the content of file is JSON format. If one of the above is incorrect asks again.

add_ticket - Asks for player credentials and checks if he exists in base. If not asks for chosen numbers, saves player and numbers to database. If player exists saves only chosen numbers. Prints confirmation info. Returns None.

lottery_result - selects random numbers based on passed file(min number, max number, quantity). Checks witch player guessed the numbers, prints his credentials and amount of the price(takes it from passed file). Divides amount of price equally between every winner. Prints 'no winner information' if nobody guessed the numbers.
