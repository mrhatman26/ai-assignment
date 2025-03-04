import ast
import pickle as pk
import numpy as np
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
    try:
        model_data = request.get_data()
        model_data = model_data.decode()
        model_data = ast.literal_eval(model_data)
        for key, value in model_data.items():
            print(str(key) + ": " + str(value) + " (" + str(type(value)) + ")", flush=True)
        #Open model files
        genre_model_file = open(get_model_path("genres", model_data["submission_model"], True), "rb")
        age_model_file = open(get_model_path("movie_rated", model_data["submission_model"], True), "rb")
        date_model_file = open(get_model_path("release_date", model_data["submission_model"], True), "rb")
        runtime_model_file = open(get_model_path("run_length", model_data["submission_model"], True), "rb")
        #Load models
        genre_model = pk.load(genre_model_file)
        age_model = pk.load(age_model_file)
        date_model = pk.load(date_model_file)
        runtime_model = pk.load(runtime_model_file)
        #Close files
        genre_model_file.close()
        age_model_file.close()
        date_model_file.close()
        runtime_model_file.close()
        #Declare output vars
        genres_output = None
        age_output = None
        date_output = None
        runtime_output = None
        #Run models
        if model_data["submission_model"] == "knn":
            #Genres model
            genres_map = load_dataset_map("genres", is_static=True)
            genres_input = input_to_map(model_data["submission_genre"], genres_map, is_bool=True)
            genres_input = np.array(list(genres_input), dtype=int)
            genres_input = genres_input.reshape(1, -1)
            genres_output = genre_model.predict(X=genres_input)
            #Age model
            age_map = load_dataset_map("movie_rated", is_static=True)
            age_input = input_to_map(model_data["submission_age"].lower(), age_map, is_bool=True)
            age_input = np.array(list(age_input), dtype=int)
            age_input = age_input.reshape(1, -1)
            age_output = age_model.predict(X=age_input)
            #Date model
            date_input = int(model_data["submission_month"]) - 1
            date_input = np.array(date_input, dtype=int)
            date_input = date_input.reshape(1, -1)
            date_output = date_model.predict(X=date_input)
            #Runtime model
            runtime_input = int(model_data["submission_runtime"])
            runtime_input = np.array(runtime_input, dtype=int)
            runtime_input = runtime_input.reshape(1, -1)
            runtime_output = runtime_model.predict(X=runtime_input)
            #Average outputs
            final_output = genres_output + age_output + date_output + runtime_output
            final_output = final_output / 4
            return str(final_output[0])
        else:
            #Genres model
            #Modify this as it won't work!
            #Get closest map to entered genres.
            genres_map = load_dataset_map("genres", is_static=True)
            genres_input = input_to_map(model_data["submission_genre"], genres_map)
            genres_input = np.array(genres_input, dtypes=int)
            genres_input = genres_input.reshape(1, -1)
            genres_output = genre_model.predict(X=genres_input)
            #Age model
            age_map = load_dataset_map("movie_rated", is_static=True)
            age_input = input_to_map(model_data["submission_age"].lower(), age_map)
            age_input = np.array(age_input, dtype=int)
            age_input = age_input.reshape(1, -1)
            age_output = age_model.predicy(X=age_input)
            #Date model
            date_input = int(model_data["submission_month"]) - 1
            date_input = np.array(date_input, dtype=int)
            date_input = date_input.reshape(1, -1)
            date_output = date_model.predict(X=date_input)
            #Runtime
            runtime_input = int(model_data["submission_runtime"])
            runtime_input = np.array(runtime_input, dtype=int)
            runtime_input = runtime_input.reshape(1, -1)
            runtime_output = runtime_model.predict(X=runtime_input)
            #Average outputs
            final_output = genres_output + age_output + date_output + runtime_output
            final_output = final_output / 4
            return str(final_output[0])
    except:
        return "failed"
    
@app.route('/predict/output/output=<output>')
def predict_output(output):
    return render_template('output.html', page_name="Movie User Rating", score=output)

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