from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://smashbros54:Meanboy6464@localhost:5432/sqlalchemyUdacity'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    administrator = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Person ID: {self.id}, Name: {self.name}>'


# back date sekof streak again
@app.route('/')
def index():
    person = Person.query.first()
    return 'Yooo Streak ' + person.name
