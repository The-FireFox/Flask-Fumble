from api4noobs import db

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

    def __repr__(self):
        return '<name %r>' % self.name