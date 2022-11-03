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

# NO TOUCHIE

def create():
    creation = input('WHAT WOULD YOU LIKE TO CREATE?(new hero/add ability to hero): ')
    if creation == 'new hero':
        hero_name = input('WHAT IS THE NAME OF THE HERO THAT IS JOINED THE AGENCY?: ')
        hero_about = input('WHAT DO YOU KNOW ABOUT THE HERO?: ')
        hero_bio = input('WHAT IS THE HEROES BACKSTORY?: ')
        query = """
            INSERT INTO heroes (name, about_me, biography)
            VALUES (%s, %s, %s);
        """
        execute_query(query, [hero_name, hero_about, hero_bio])
        print(f"THE DIRECTOR WELCOMES {hero_name} INTO THE AGENCY")
        print('QUERY COMPLETE, RETURNING TO ACCESS PORT')
        director_action()
    elif creation == 'add ability to hero':
        hero_id = input('WHAT IS THE NUMERICAL IDENTIFICATION OF THE HERO?: ')
        ability_type = input('WHAT ABILITIES DOES THE HERO POSSES?(REFERENCE ABILITY_TYPE TABLE): ')
        query = """
            INSERT INTO abilities (hero_id, ability_type_id)
            VALUES (%s, %s);
        """
        execute_query(query, [hero_id, ability_type])
        print(f"HERO'S ABILITY ADDED")
        print('QUERY COMPLETE, RETURNING TO ACCESS PORT')
        director_action()

def read():
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
    z = input('WHAT INFORMATION WOULD YOU LIKE TO KNOW?(abilities/relationships): ')
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
    elif z == 'relationships':
        query = """
            SELECT h1.name, relationship_types.name, h2.name
            FROM relationships
            JOIN heroes h1 ON h1.id = relationships.hero1_id
            JOIN heroes h2 ON h2.id = relationships.hero2_id
            JOIN relationship_types ON relationship_types.id = relationships.relationship_type_id
        """
        list_of_heroes = execute_query(query).fetchall()
        for record in list_of_heroes:
                print('')
                print(record[0] + ' ' + 'is a' + ' ' + record[1] + ' ' + 'with' + ' ' + record[2])
    else: print('INVALID, EXIT PROTOCOL INITIATED')
    print('QUERY COMPLETE, RETURNING TO ACCESS PORT')
    director_action()

def update():
    update_info = input('WHAT WOULD YOU LIKE TO CHANGE?(name): ')
    if update_info == 'name':
        which_hero = input('WHICH HERO IS CHANGING THERE IDENTITY?(REFERENCE HERO(ID) TABLE): ')
        new_hero_name = input('WHAT IS THE NEW IDENTITY OF THE HERO?: ')
        query = """
            UPDATE heroes
            SET name = %s
            WHERE id = %s
        """
        execute_query(query, [new_hero_name, which_hero])
        print(f"THE AGENCY NOW RECOGNIZES {new_hero_name}")
        print('QUERY COMPLETE, RETURNING TO ACCESS PORT')
        director_action()

def delete():
    hero_death = input('I AM SORRY TO HEAR THAT DIRECTOR, WHICH HERO HAS PERISHED?: ')
    query = """
        DELETE FROM heroes WHERE name = %s
    """
    execute_query(query, [hero_death,])
    print(f"{hero_death} WILL NOT HAVE DIED IN VAIN. {hero_death} WILL BE REMEMBERED")
    print('QUERY COMPLETE, RETURNING TO ACCESS PORT')
    director_action()

def director_action():
    crud_input = input('WHAT WOULD YOU LIKE TO DO TODAY DIRECTOR?(create/read/update/delete): ')
    if crud_input == 'create':
        create()
    elif crud_input == 'read':
        read()
    elif crud_input == 'update':
        update()
    elif crud_input == 'delete':
        delete()

def main_terminal():
    director_input = input('WHO IS ACCESSING THE TERMINAL: ')
    if director_input == 'director':
        director_action()
    else:
        print('ACCESS DENIED')
        i = 1
        while i < 11:
            print('CONTACTING AUTHORITIES')
            i += 1
        print('PORT TERMINATED')
main_terminal() 



# def basic_info():
#     x = input('WHO IS ACCESSING THE TERMINAL: ')
#     print('hello ' + x)
#     if x == 'director':
#         a = input('WHAT WOULD YOU LIKE TO DO DIRECTOR?(create/read/update/delete): ')
#         if a == 'read':
#             y = input('WOULD YOU LIKE TO SEE A CURRENT LIST OF ACTIVE HEROES? (y/n): ')
#             if y == 'y':
#                 query = """
#                     SELECT heroes.name 
#                     FROM heroes
#                 """
#                 list_of_heroes = execute_query(query).fetchall()
#                 for record in list_of_heroes:
#                         print('')
#                         print(record[0])
#             else: print('OK')
#             z = input('WHAT INFORMATION WOULD YOU LIKE TO KNOW?(abilities): ')
#             if z == 'abilities':
#                 query = """
#                     SELECT heroes.name, ability_types.name 
#                     FROM heroes
#                     JOIN abilities ON heroes.id = abilities.hero_id
#                     JOIN ability_types ON ability_types.id = abilities.ability_type_id 
#                 """
#                 list_of_heroes = execute_query(query).fetchall()
#                 for record in list_of_heroes:
#                         print('')
#                         print(record[0] + ' ' + record[1])
#             else: print('INVALID, EXIT PROTOCOL INITIATED')
#             print('QUERY COMPLETE, RETURNING TO ACCESS PORT')
#             basic_info()
#         elif a == 'create':
#             creation = input('WHAT WOULD YOU LIKE TO CREATE?(new hero/new ability): ')
#             if creation == 'new hero':
#                 hero_name = input('WHAT IS THE NAME OF THE HERO THAT IS JOINED THE AGENCY?: ')
#                 hero_about = input('WHAT DO YOU KNOW ABOUT THE HERO?: ')
#                 hero_bio = input('WHAT IS THE HEROES BACKSTORY?: ')
#                 query = """
#                     INSERT INTO heroes (name, about_me, biography)
#                     VALUES (%s, %s, %s);
#                 """
#                 execute_query(query, [hero_name, hero_about, hero_bio])
#                 print(f"THE DIRECTOR WELCOMES {hero_name} INTO THE AGENCY")
#                 print('QUERY COMPLETE, RETURNING TO ACCESS PORT')
#                 basic_info()
#             elif creation == 'new ability':
#                 hero_id = input('WHAT IS THE NUMERICAL IDENTIFICATION OF THE HERO?: ')
#                 ability_type = input('WHAT ABILITIES DOES THE HERO POSSES?(REFERENCE ABILITY_TYPE TABLE): ')
#                 query = """
#                     INSERT INTO abilities (hero_id, ability_type_id)
#                     VALUES (%s, %s);
#                 """
#                 execute_query(query, [hero_id, ability_type])
#                 print(f"HERO'S ABILITY ADDED")
#                 print('QUERY COMPLETE, RETURNING TO ACCESS PORT')
#                 basic_info()
#         elif a == 'update':
#             update_info = input('WHAT WOULD YOU LIKE TO CHANGE?(name): ')
#             if update_info == 'name':
#                 which_hero = input('WHICH HERO IS CHANGING THERE IDENTITY?(REFERENCE HERO(ID) TABLE): ')
#                 new_hero_name = input('WHAT IS THE NEW IDENTITY OF THE HERO?: ')
#                 query = """
#                     UPDATE heroes
#                     SET name = %s
#                     WHERE id = %s
#                 """
#                 execute_query(query, [new_hero_name, which_hero])
#                 print(f"THE AGENCY NOW RECOGNIZES {new_hero_name}")
#                 print('QUERY COMPLETE, RETURNING TO ACCESS PORT')
#                 basic_info()
#         elif a == 'delete':
#             hero_death = input('I AM SORRY TO HEAR THAT DIRECTOR, WHICH HERO HAS DIED?: ')
#             query = """
#                 DELETE FROM heroes WHERE name = %s
#             """
#             execute_query(query, [hero_death,])
#             print(f"{hero_death} WILL BE REMEMBERED")
#             print('QUERY COMPLETE, RETURNING TO ACCESS PORT')
#             basic_info()
#     else: print('ACCESS DENIED, CALLING AUTHORITIES')
# basic_info()

