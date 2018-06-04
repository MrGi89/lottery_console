from psycopg2 import connect

players_table = '''CREATE TABLE players(
                                        player_id serial NOT NULL, 
                                        first_name varchar(64) NOT NULL, 
                                        last_name varchar(64) NOT NULL, 
                                        PRIMARY KEY(player_id));'''

tickets_table = '''CREATE TABLE tickets(
                                        ticket_id serial NOT NULL,
                                        numbers smallint[] NOT NULL,  
                                        player_id integer NOT NULL, 
                                        FOREIGN KEY(player_id) REFERENCES players(player_id) ON DELETE CASCADE);'''

cnx = connect(
    user='postgres',
    password='coderslab',
    host='localhost',
    database='kadeor')
cnx.autocommit = True
cursor = cnx.cursor()
cursor.execute(players_table)
cursor.execute(tickets_table)
cursor.close()
cnx.close()
