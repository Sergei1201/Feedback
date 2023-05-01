# Import all dependencies for the app
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

# Initialize app by instantiating Flask class (create app object)
app = Flask(__name__)

# Define an environment variable
ENV = 'dev'

# Establish a connection to Postgres based of whatever environment variable is set up
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/lexus'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Instantiate SQLAlchemy class
db = SQLAlchemy(app)

# Define feedback class


class Feedback(db.Model):
    # Define properties
    __feedback__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    # Create a constructor
    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


# Create a table in the database
with app.app_context():
    db.create_all()

# Define routes for the app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Make sure the method is POST
    if request.method == 'POST':
        # Assign variables from the form fields
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please fill all fields')
        # Check if there's a comment that has already been submitted by the customer (in other words check if the customer already exist in the database, if he doesn't, add feedback to the database)
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            # Instantiate new feedback with constructor
            data = Feedback(customer, dealer, rating, comments)
            # Add data to the session
            db.session.add(data)
            # Commit to the database
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message='Feedback has already been submitted')


# Running the development server
if __name__ == '__main__':
    app.run()
