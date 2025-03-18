from flask import Flask, render_template, request, redirect, url_for, session, flash

# Class for creating games
class Game:
    def __init__(self, name, category, company):
        self.name = name
        self.category = category
        self.company = company

# Library class to manage the games
class Library:
    def __init__(self):
        self.list = [
            Game('Metroid', 'Metroidvania', 'Nintendo'),
            Game('Zelda', 'Adventure', 'Nintendo'),
            Game('Red Dead Redemption','Action-Adventure', 'Rockstar Games')
        ]

    def add_game(self, game):
        self.list.append(game)

    def remove_game(self, game):
        self.list.remove(game)

    def get_games(self):
        return self.list


library_instance = Library()  # Calls the library functions, no magic here

# Dummy users for testing purposes, no hamsters were harmed during this process
class User:
    def __init__(self, id, nickname, password):
        self.id = id
        self.nickname = nickname
        self.password = password

user1 = User('1', 'Gustavo Ayres', 'welcome')  # A pro at passwords, as you can see
user2 = User('2', 'Alice Miller', 'hamsters')  # We don’t judge here
user3 = User('3', 'Jason Smith', 'password123')  # Classic, right?

users = {
    user1.nickname: user1,
    user2.nickname: user2,
    user3.nickname: user3
}

app = Flask(__name__)
app.secret_key = 'hardpassword'  # Because who needs an easy one?

@app.route('/')
def index():
    # Just rendering home.html and showing the game list
    games = library_instance.get_games()
    return render_template('lista.html', title='Game', game_list=games)

@app.route('/new')
def new():
    # If the user isn't logged in, they’re blocked from accessing this page
    if 'logged_in_user' not in session or session['logged_in_user'] == None:
        return redirect(url_for('login', next=url_for('new')))  # Redirect with the next page

    return render_template('new.html', title='New Game')  # Show new game page

@app.route('/create', methods=['POST'])  # Just creating a new game.
def create():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']

    new_game = Game(name, category, console)
    # Calls the instance to add the new game
    library_instance.add_game(new_game)

    return redirect(url_for('index'))  # Redirects to home

@app.route('/login')
def login():
    next_page = request.args.get('next')  # Captures the next page URL
    return render_template('login.html', next=next_page)

@app.route('/auth', methods=['POST'])
def auth():
    # Variables for user and password
    user_typed = request.form['user']
    password_typed = request.form['password']

    # Checks if user exists in the 'users' dictionary
    if user_typed in users:
        user_obj = users[user_typed]
        
        # Verifies if the password typed matches the one in the user object
        if password_typed == user_obj.password:
            # Creates a session for the user
            session['logged_in_user'] = user_typed
            flash(f'User {user_obj.nickname} successfully logged in!')
            # Gets 'next' from <form>, with fallback to the homepage
            next_page = request.form['next']
            return redirect(next_page or url_for('index'))
    else:
        flash('Incorrect password, try again!')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    # Removes the user from the session
    session.pop('logged_in_user', None)
    flash('Successfully logged out!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
