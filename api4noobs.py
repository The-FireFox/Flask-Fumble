from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'hardpassword' # Because who needs an easy one?

app.config['SQLALCHEMY_DATABASE_URI'] = \
       '{SGBD}://{user}:{password}@{host}/{database}'.format(
           SGBD = 'mysql+mysqlconnector',
           user = 'main_root',
           password = 'welcome',
           host = 'localhost',
           database = 'api4noobs'
       )

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class games(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(40), nullable=False)
    company = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<name %r>' % self.name

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nickname = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(20), nullable=False)

@app.route('/')
def index():
    # Just rendering home.html and showing the game list
    list = games.query.order_by(games.id)
    return render_template('list.html', title='Game', game_list=list)

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
    company = request.form['company']

    games = games.query.filter_by(name=name).first()
    if games:# Verifies if the game already exists
        flash('Game already exists!')
        return redirect(url_for('new'))
    
    new_game = games(name=name, category=category, company=company)
    db.session.add(new_game) # Adds the new game to the database
    db.session.commit() # Commits the changes
    flash('Game created successfully!') # yay!

    return redirect(url_for('index'))  # Redirects to home

@app.route('/login')
def login():
    next_page = request.args.get('next')  # Captures the next page URL
    return render_template('login.html', next=next_page)

@app.route('/auth', methods=['POST',]) # Checks if user exists in the 'users' dictionary
def auth():
    user = users.query.filter_by(nickname=request.form['nickname']).first()
    if user: # Verifies if the user exists
        if request.form['password'] == user.password: # Verifies if the password matches the one in the user
            session['logged_in_user'] = user.nickname
            flash(f'User {user.nickname} successfully logged in!')
            next_page = request.form.get('next','')
            return redirect(next_page if next_page else url_for('index')) # Gets 'next' from <form>, with fallback to the homepage
    else: # If the user doesn't exist, it shows an error message
        flash('Incorrect password or user, try again!')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    # Removes the user from the session
    session.pop('logged_in_user', None)
    flash('Successfully logged out!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
