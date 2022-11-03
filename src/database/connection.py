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
    creation = input('WHAT WOULD YOU LIKE TO CREATE?(new hero/add ability to hero/new ability discovered): ')
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
        print("HERO'S ABILITY ADDED")
        print('QUERY COMPLETE, RETURNING TO ACCESS PORT')
        director_action()
    elif creation == 'new ability discovered':
        ability_create = input('WHAT NEW ABILITY HAS THE AGENCY DISCOVERED?: ')
        query = """
            INSERT INTO ability_types (name)
            VALUES (%s)
        """
        execute_query(query, [ability_create,])
        print(f"INTERESTING, THE SCIENCE TEAM WILL NEED TO STUDY {ability_create}")
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
            SELECT heroes.name, STRING_AGG(ability_types.name, ', ') 
            FROM heroes
            JOIN abilities ON heroes.id = abilities.hero_id
            JOIN ability_types ON ability_types.id = abilities.ability_type_id 
            GROUP BY heroes.name
        """
        list_of_heroes = execute_query(query).fetchall()
        for record in list_of_heroes:
                print('')
                print(record[0] + ' ' + record[1])
        director_action()
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

def omegaalpha():
    last_warning = input('ARE YOU ABSOLUTELY SURE YOU WANT TO INITIATE SECURITY PROTOCOL OMEGA_ALPHA?(y/n): ')
    if last_warning == 'y':
        print('IT WAS A PLEASURE WORKING WITH YOU DIRECTOR')
        secret_code = input('ENTER YOUR PERSONAL SECURITY CODE TO VERIFY: ')
        if secret_code == 'LaLiLuLeLo':
            query = """
                DELETE FROM abilities
                DELETE FROM ability_types
                DELETE FROM heroes
                DELETE FROM relationship_types
                DELETE FROM relationships
            """
            execute_query(query)
            print('GOODBYE')
        else: print('WRONG CODE, SYSTEM LOCKING TO PREVENT DATA LOSS AND BREACH')
    else: director_action()
    
def director_action():
    crud_input = input('WHAT WOULD YOU LIKE TO DO TODAY DIRECTOR?(create/read/update/delete/system compromised): ')
    if crud_input == 'create':
        create()
    elif crud_input == 'read':
        read()
    elif crud_input == 'update':
        update()
    elif crud_input == 'delete':
        delete()
    elif crud_input == 'system compromised':
        omegaalpha()

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



# group by heroes.name
# concat