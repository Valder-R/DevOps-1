from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    review = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Review %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'review': self.review,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S')
        }

with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        review_text = request.form['review']

        review = Review(username=username, review=review_text)

        try:
            db.session.add(review)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return str(e)
    else:
        return render_template("index.html")

@app.route('/reviews', methods=['GET'])
def reviews():
    reviews = Review.query.order_by(Review.id.desc()).all()
    return render_template("reviews.html", reviews=reviews)


@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    reviews_api = Review.query.order_by(Review.date.desc()).all()
    return jsonify([r.to_dict() for r in reviews_api]), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

