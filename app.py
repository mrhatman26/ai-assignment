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
    genres = load_dataset_map("genres")
    for i in range(0, len(genres)):
        genres[i] = genres[i].title()
    return render_template('submit.html', page_name="Submit Data", genres=genres)

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