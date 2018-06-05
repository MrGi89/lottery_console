import json
import os
from random import randrange
from psycopg2 import connect, ProgrammingError
from psycopg2.extras import RealDictCursor


def sql_execute(sql):
    '''Function responsible for connecting to database and executing given SQL command.
        Args:
              sql(str) - SQL command.
        Returns:
              If the searched value exists function returns tuple with dictionaries containing founded values,
              otherwise returns None.
    '''
    cnx = connect(
        user='postgres',
        password='coderslab',
        host='localhost',
        database='kadeor',
    )
    cnx.autocommit = True
    cursor = cnx.cursor(cursor_factory=RealDictCursor)
    cursor.execute(sql)
    try:
        result = cursor.fetchall()
    except ProgrammingError:
        result = None
    cursor.close()
    cnx.close()
    return result


def add_ticket():
    '''Asks for player credentials and checks if he exists in base.
    If not asks for chosen numbers, saves player and numbers to database.
    If player exists saves only chosen numbers.
    Prints confirmation info. Returns None.
    '''
    first_name = input('Enter your first name:').strip()
    last_name = input('Enter your last name:').strip()
    player = sql_execute('''SELECT * FROM players 
                            WHERE first_name ILIKE '{}' AND last_name ILIKE '{}';'''.format(first_name, last_name))
    if not player:
        player = sql_execute('''INSERT INTO players(first_name, last_name) 
                                VALUES('{}', '{}') RETURNING *;'''.format(first_name, last_name))
        print('Welcome to the Lottery. Select {} numbers from {} to {}. '
              'If all the numbers chosen by you will match the numbers drawn in the lottery, '
              'you can win up to {}'. format(numbers_quantity, min_allowed, max_allowed, prize_pool))
    else:
        print('Welcome back {} {}!!!'.format(player[0]['first_name'], player[0]['last_name']))
        saved_numbers = sql_execute('''SELECT numbers FROM tickets WHERE player_id={}'''.format(player[0]['player_id']))
        if saved_numbers:
            print('So far you selected:')
            for number in saved_numbers:
                print(number['numbers'])
    player_numbers = []
    while len(player_numbers) < numbers_quantity:
        try:  # checks if type of passed argument is an integer.
            chosen_number = int(input('Add your {} number:'.format(len(player_numbers) + 1)))
        except ValueError:
            print('Please select a number between {} - {}'.format(min_allowed, max_allowed))
            continue
        if chosen_number < min_allowed or chosen_number > max_allowed:  # checks if passed number is in correct range.
            print('Please select a number between {} - {}'.format(min_allowed, max_allowed))
        else:
            player_numbers.append(chosen_number)
    player_numbers.sort()
    sql_execute('''INSERT INTO tickets(numbers, player_id) 
                   VALUES (ARRAY{}, {}); '''.format(player_numbers, player[0]['player_id']))
    print('Your ticket has been added correctly. Chosen numbers {}'.format(player_numbers))

                                                                                
def lottery_result():
    '''Selects random numbers based on passed file(min number, max number, quantity).
    Checks witch player guessed the numbers, prints his credentials and amount of the price(takes it from passed file).
    Divides amount of price equally between every winner. Prints 'no winner information' if nobody guessed the numbers.
    '''
    draw_result = [randrange(min_allowed, max_allowed + 1) for _ in range(numbers_quantity)]
    draw_result.sort()
    winning_tickets = sql_execute('''SELECT * FROM tickets WHERE numbers=ARRAY{}::smallint[];'''.format(draw_result))
    if winning_tickets:
        price = prize_pool / len(winning_tickets)
        for ticket in winning_tickets:
            winner = sql_execute('''SELECT * FROM players WHERE player_id='{}';'''.format(ticket['player_id']))
            print('{} {} won {}'.format(winner[0]['first_name'], winner[0]['last_name'], '{0:.2f}'.format(price)))
    else:
        print('There was no winners')


def check_file():
    '''Asks for directory of file. Checks if the path is correct and whether the content of file is JSON format.
    If one of the above is incorrect asks again.
    '''
    while True:
        path = input('Enter path to file: ')
        if os.path.isfile(path):  # checks if given path leads to file.
            with open(path) as file:
                try:  # checks if file content is in JSON format.
                    file_content = json.load(file)
                    print('File loaded successfully.')
                    return file_content
                except json.JSONDecodeError:
                    print('Content of the file should be in JSON format. Please try again.')
                    continue
        else:
            print('File does not exists. Please try again.')
            continue


json_data = check_file()
numbers_quantity = int(json_data['numbers-quantity'])
prize_pool = int(json_data['prize-pool'])
min_allowed = int(json_data['numbers-range']['min'])
max_allowed = int(json_data['numbers-range']['max'])
