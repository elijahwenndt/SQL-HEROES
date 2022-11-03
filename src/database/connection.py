import psycopg
from psycopg import OperationalError

def create_connection(db_name, db_user, db_password, db_host = "localhost", db_port = "5432"):
    connection = None
    try:
        connection = psycopg.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(query, params=None):
    connection = create_connection("postgres", "postgres", "postgres")
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        print("Query executed successfully")
        connection.close()
        return cursor
    except OSError as e:
        print(f"The error '{e}' occurred or the hero name is already taken")

# DO NOT TOUCH FILE ABOVE

# def select_all():
#     query = """
#         SELECT * from heroes
#     """

#     list_of_heroes = execute_query(query).fetchall()
#     print(list_of_heroes)
#     for record in list_of_heroes:
#         print(record[1])

# select_all()

def basic_info():
    x = input('WHO IS ACCESSING THE TERMINAL: ')
    print('hello ' + x)
    if x == 'director':
        a = input('WHAT WOULD YOU LIKE TO DO DIRECTOR?(CREATE/READ): ')
        if a == 'read':
            y = input('WOULD YOU LIKE TO SEE A CURRENT LIST OF ACTIVE HEROES? (y/n): ')
            if y == 'y':
                query = """
                    SELECT heroes.name 
                    FROM heroes
                """
                list_of_heroes = execute_query(query).fetchall()
                for record in list_of_heroes:
                        print('')
                        print(record[0])
            else: print('OK')
            z = input('WHAT INFORMATION WOULD YOU LIKE TO KNOW?(abilities): ')
            if z == 'abilities':
                query = """
                    SELECT heroes.name, ability_types.name 
                    FROM heroes
                    JOIN abilities ON heroes.id = abilities.hero_id
                    JOIN ability_types ON ability_types.id = abilities.ability_type_id 
                """
                list_of_heroes = execute_query(query).fetchall()
                for record in list_of_heroes:
                        print('')
                        print(record[0] + ' ' + record[1])
            else: print('INVALID')
        elif a == 'create':
            hero_name = print('WHAT IS THE NAME OF THE HERO THAT IS JOINED THE AGENCY?: ')
            hero_about = print('WHAT DO YOU KNOW ABOUT THE HERO?: ')
            hero_bio = print('WHAT IS THE HEROES BACKSTORY?: ')
            query = """
                INSERT INTO heroes (name, about_me, biography)
                VALUES (%s, %s, %s);
            """
            execute_query(query, [hero_name, hero_about, hero_bio])
            print(f"THE DIRECTOR WELCOMES {hero_name} INTO THE AGENCY")
    else: print('ACCESS DENIED, CALLING AUTHORITIES')
basic_info()

# SELECT heroes.name, ability_types.name 
#                 FROM heroes
#                 JOIN abilities ON heroes.id = abilities.hero_id
#                 JOIN ability_types ON ability_types.id = abilities.ability_type_id