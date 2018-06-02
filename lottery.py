import json
from psycopg2 import connect, ProgrammingError
from psycopg2.extras import RealDictCursor


with open('zadanie.json') as file:
    json_data = json.load(file)

numbers_quantity = int(json_data['numbers-quantity'])
prize_pool = int(json_data['prize-pool'])
min_allowed = int(json_data['numbers-range']['min'])
max_allowed = int(json_data['numbers-range']['max'])


def sql_execute(sql):

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

    first_name = input('Enter your first name:')
    last_name = input('Enter your last name:')

    player = sql_execute('''SELECT * FROM players 
                            WHERE first_name='{}' AND last_name='{}';'''.format(first_name, last_name))

    if not player:
        player = sql_execute('''INSERT INTO players(first_name, last_name) 
                                VALUES('{}', '{}') RETURNING *;'''.format(first_name, last_name))

    player_numbers = []

    while len(player_numbers) < numbers_quantity:
        chosen_number = int(input('Add your {} number:'.format(len(player_numbers) + 1)))
        if max_allowed < chosen_number < min_allowed:
            print('Numer should be between {} - {}'.format(min_allowed, max_allowed))
        else:
            player_numbers.append(chosen_number)

    sql_execute('''INSERT INTO tickets(numbers, player_id) 
                   VALUES (ARRAY{}, {}); '''.format(player_numbers, player[0]['player_id']))

    print('Your ticket has been added correctly. Chosen numbers{}'.format(player_numbers))

                                                                                
def lottery_result():
    pass


if __name__ == '__main__':
    add_ticket()
