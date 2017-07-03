import requests
import psycopg2
import os


def execute_sql_statement(sql_statement, values=tuple()):
    connect_str = "dbname=szabadon user=szabadon host=localhost password=pringles"
    # setup connection string, not the most secure way
    # we create this variable by assigning a None value to it,
    # so when an Exception is catched, the function will not try to close a non-existing variable
    conn = None
    try:
        # use our connection values assigned to the connection string to establish a connection
        # Hey dawg, I heard you like connection, so I put your connection values into your connection string to
        # use them to establish a connection
        conn = psycopg2.connect(connect_str)
    except psycopg2.DatabaseError as e:  # TODO don't use this, remember: "raise PythonicError("Errors should never go silently.")
        print(e)
        return [[e]]
    else:
        conn.autocommit = True
        cursor = conn.cursor()
        try:
            cursor.execute(sql_statement, values)
        except psycopg2.ProgrammingError as e:
            print(e)
            return [[e]]
        else:
            if sql_statement.split(' ')[0].lower() == 'select':
                rows = list(cursor.fetchall())
                return rows
    finally:
        if conn:
            # conn.commit() leaving it here for future testing to see how it works
            conn.close()


def get_swapi_response(URL):
    planets = requests.get(URL).json()
    planets_results = planets['results']
    previous_page = planets['previous']
    next_page = planets['next']
    attributes_we_need = ['name', 'diameter', 'climate', 'terrain', 'surface_water', 'population', 'residents']
    page_data = []
    for planet_details in planets_results:
        page_data.append([planet_details[attribute] for attribute in attributes_we_need])
    return [page_data, previous_page, next_page]
