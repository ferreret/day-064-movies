from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import tmdb


app = Flask(__name__)
app.config['SECRET_KEY'] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)


class MovieEditForm(FlaskForm):
    rating = StringField("Your Rating Out of 10, e.g. 7.5",
                         validators=[DataRequired()])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")


class MovieAddForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


@ app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating).all()

    for i in range(len(all_movies)):
        # This line gives each movie a new ranking reversed from their order in all_movies
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    return render_template("index.html",
                           movies=all_movies)


@ app.route("/edit/<int:movie_id>", methods=("GET", "POST"))
def rate_movie(movie_id):
    form = MovieEditForm()
    if form.validate_on_submit():
        movie_to_edit = Movie.query.get(movie_id)
        new_rating = float(form.rating.data)
        new_review = form.review.data
        movie_to_edit.rating = new_rating
        movie_to_edit.review = new_review
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=form)


@app.route("/delete/<int:movie_id>", methods=["GET"])
def delete_movie(movie_id):
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=("GET", "POST"))
def add_movie():
    form = MovieAddForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        # TODO Here I have to search  movie info
        search_list = tmdb.get_movies_by_title(movie_title)
        return render_template("select.html", movies=search_list)
    return render_template("add.html", form=form)


@app.route("/add_selected_movie/<int:movie_id>")
def add_selected_movie(movie_id):
    movie_info = tmdb.get_movie_details(movie_id)
    if movie_info:
        db.session.add(
            Movie(
                id=movie_id,
                title=movie_info.title,
                year=movie_info.year(),
                description=movie_info.description,
                img_url=movie_info.img_url,
                rating=0,
                ranking=0,
                review=""
            ))
        print(movie_info.img_url)
        db.session.commit()
    return redirect(url_for("rate_movie", movie_id=movie_id))


if __name__ == '__main__':
    app.run(debug=True)
