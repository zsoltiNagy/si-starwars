from flask import Flask, render_template, request, redirect, url_for, json
from data_handler import get_swapi_response, execute_sql_statement
from constants import PLANETS, PLANET_ATTRIBUTES, PEOPLE_ATTRIBUTES, USER, PREVIOUS_URL, NEXT_URL

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def root():
    global NEXT_URL
    global PREVIOUS_URL
    if request.method == 'POST':
        if request.form['direction'] == 'Previous' and PREVIOUS_URL:
            response = get_swapi_response(PREVIOUS_URL)
        elif request.form['direction'] == 'Next' and NEXT_URL:
            response = get_swapi_response(NEXT_URL)
        else:
            response = get_swapi_response('https://swapi.co/api/planets/?page=1')
    elif request.method == 'GET':
        response = get_swapi_response('https://swapi.co/api/planets/?page=1')
    PREVIOUS_URL = response[1]
    NEXT_URL = response[2]
    # voteStat = execute_sql_statement("""SELECT planetname, COUNT(planetname) FROM starwars_planets GROUP BY planetname;""")
    # voteStat = ",".join("(%s,%s)" % tup for tup in voteStat).replace('(', '{').replace(')', '}')
    return render_template('table.html',
                           user=USER,
                           planets=response[0],
                           planet_attributes=PLANET_ATTRIBUTES,
                           people_attributes=PEOPLE_ATTRIBUTES,
                           previous=PREVIOUS_URL,
                           next=NEXT_URL)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        header = "Welcome! Please fill out the following form to make a new user."
        return render_template('registration.html', header=header)
    elif request.method == 'POST':
        if request.args.get('password') == request.args.get('second_password'):
            new_username = request.form['username']
            new_password = request.form['password']
            check_username = execute_sql_statement("""SELECT username FROM starwars_users
                                                   WHERE username = %s""",
                                                   (new_username,))
            if check_username:
                header = "This username is taken, please try again!"
                return render_template('registration.html', header=header)
            else:
                execute_sql_statement("""INSERT INTO starwars_users (username, password) VALUES (%s, %s)""",
                                      (new_username, new_password))
                header = "Succesful registration! Please login:"
                return render_template('login.html', header=header)
        else:
            header = "The two passwords didn't match, please try again!"
            return render_template('registration.html', header=header)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        header = "Please login:"
        return render_template('login.html', header=header)
    elif request.method == 'POST':
        login_username = request.form['login_username']
        login_password = request.form['login_password']
        db_response = execute_sql_statement("""SELECT username FROM starwars_users
                                               WHERE username = %s AND password = %s""",
                                            (login_username, login_password))
        if db_response:
            global USER
            USER = db_response[0][0]
            return redirect(url_for('root'))
        else:
            header = "Wrong username or password. Please try again!"
            return render_template('login.html', header=header)


@app.route('/logout')
def logout():
    global USER
    USER = 'guest'
    header = "You successfully logged out!"
    return render_template('login.html', header=header)


@app.route('/votePlanet', methods=['POST'])
def votePlanet():
    user = request.form['username']
    planet = request.form['planet']
    already_voted_on_this_planet = execute_sql_statement("""SELECT * FROM starwars_planets
                                                         WHERE username = %s and planetname= %s""",
                                                         (user, planet))
    if not already_voted_on_this_planet:
        execute_sql_statement("""INSERT INTO starwars_planets (planetname, username)
                              VALUES (%s, %s)""",
                              (planet, user))
        return json.dumps('You succesfully voted on ' + str(planet))
    return json.dumps('You already voted on ' + str(planet))


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
