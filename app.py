import ast
from flask import Flask, render_template, url_for, request, redirect, abort
from misc import *

'''Check models and maps exist'''
check_and_move_models_knn()
check_and_move_models_linear()
check_and_move_maps()

'''Server Vars'''
app = Flask(__name__)
deployed = False

'''General Routes'''
@app.route('/')
def home():
    return render_template('home.html', page_name="IMDb Rating Predictor")

@app.route('/predict/submit/')
def predict_submit():
    genres = load_dataset_map("genres", is_static=True)
    for i in range(0, len(genres)):
        genres[i] = genres[i].title()
    age_ratings = load_dataset_map("movie_rated", is_static=True)
    for i in range(0, len(age_ratings)):
        age_ratings[i] = age_ratings[i].title()
    return render_template('submit.html', page_name="Submit Data", genres=genres, age_ratings=age_ratings)

@app.route('/predict/validate/', methods=['POST'])
def predict_validate():
    model_data = request.get_data()
    model_data = model_data.decode()
    model_data = ast.literal_eval(model_data)
    for key, value in model_data.items():
        print(str(key) + ": " + str(value) + " (" + str(type(value)) + ")", flush=True)
    print(type(model_data["submission_genre"]), flush=True)
    return redirect('/')

'''Error Pages'''
@app.errorhandler(404)
def page_invalid(e):
    return render_template('errors/404.html'), 404
@app.errorhandler(405)
def page_wrong_method(e):
    abort(404)

'''Favicon Supression'''
@app.route('/favicon.ico')
def favicon():
    return url_for("static", filename="favicon.ico")

if __name__ == '__main__':
    if deployed is True:
        from waitress import serve
        serve(app, host="0.0.0.0", port=5000)
    else:
        app.run(host="0.0.0.0", debug=True)