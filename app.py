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
deployed = True

'''General Routes'''
@app.route('/')
def home():
    return render_template('home.html', page_name="IMDb Rating Predictor")

@app.route('/predict/submit/')
def predict_submit():
    #This is the submit page, it allows the user to submit information about their film
    #for the model to predict the user score with.
    #This page is handled by submission.js.
    #Load both dataset maps and make sure all elements inside are titled.
    genres = load_dataset_map("genres", is_static=True)
    for i in range(0, len(genres)):
        genres[i] = genres[i].title()
    age_ratings = load_dataset_map("movie_rated", is_static=True)
    for i in range(0, len(age_ratings)):
        age_ratings[i] = age_ratings[i].title()
    return render_template('submit.html', page_name="Submit Data", genres=genres, age_ratings=age_ratings)

@app.route('/predict/validate/', methods=['POST'])
def predict_validate():
    #This route handles the models.
    #It takes the data given to it by submission.js and uses it on the models.
    #It requires the POST method to recieve data.
    try:
        model_data = request.get_data()
        model_data = model_data.decode()
        model_data = ast.literal_eval(model_data)
        #ast.literal_eval takes the recieved request data and converts it to a dictionary.
        #The list inside this data (that of the genres) is also converted back into a list.
        #This is needed because the request, once decoded, is plain text stored as an string.
        #Open model files from static directory
        genre_model_file = open(get_model_path("genres", model_data["submission_model"], True), "rb")
        age_model_file = open(get_model_path("movie_rated", model_data["submission_model"], True), "rb")
        date_model_file = open(get_model_path("release_date", model_data["submission_model"], True), "rb")
        runtime_model_file = open(get_model_path("run_length", model_data["submission_model"], True), "rb")
        #Load models using pickle.
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
        #If the user selected "knn", the K-Nearest Neighbours models will be used,
        #else, the Linear Regression models will be used.
        if model_data["submission_model"] == "knn":
            #Genres model
            genres_map = load_dataset_map("genres", is_static=True) #Get the genres map form the static directory.
            #Convert the user's input a binary list which is the same as the data used to train the model.
            #Each binary number represents one genre, so if it is 1, the movie has that genre. Same with the user's input.
            genres_input = input_to_map(model_data["submission_genre"], genres_map, is_bool=True)
            #Convert the user's inputed (now binary list) into a numpy array.
            #Then reshape the array to be 1 x value (1) and no y values (-1).
            genres_input = np.array(list(genres_input), dtype=int)
            genres_input = genres_input.reshape(1, -1)
            #Pass the input to the genre model for prediction.
            #Save the output as genres_output.
            genres_output = genre_model.predict(X=genres_input)
            #Age model
            age_map = load_dataset_map("movie_rated", is_static=True) #Get the ages map from the static directory.
            #The same as the genre's input_to_map, but the inputted data is made to be all lowercase.
            age_input = input_to_map(model_data["submission_age"].lower(), age_map, is_bool=True)
            age_input = np.array(list(age_input), dtype=int)
            age_input = age_input.reshape(1, -1)
            #Pass the input to the age model for prediciton.
            #Save the ouput as age_output.
            age_output = age_model.predict(X=age_input)
            #Date model
            #Get the user's inputted day of the month and reduce it by one to avoid index errors.
            date_input = int(model_data["submission_month"]) - 1
            date_input = np.array(date_input, dtype=int)
            date_input = date_input.reshape(1, -1)
            #Pass the input to the date model for prediction.
            #Save the output as date_output.
            date_output = date_model.predict(X=date_input)
            #Runtime model
            #The runtime input does not need modifying and is passed as is to the model after being made a numpy array.
            runtime_input = int(model_data["submission_runtime"])
            runtime_input = np.array(runtime_input, dtype=int)
            runtime_input = runtime_input.reshape(1, -1)
            #Pass the input to the age model for prediction.
            #Save the output as runtime_model.
            runtime_output = runtime_model.predict(X=runtime_input)
            #Average outputs
            #Get the average user rating from all of the model outputs.
            final_output = genres_output + age_output + date_output + runtime_output
            final_output = final_output / 4
            #Return the average rating to submission.js, rounded to 2 decimal places, to show to the user.
            return str(round(final_output[0], 2))
        else:
            #Genres model
            #Get both the normal and boolean maps for the genres from the static directory.
            genres_map = load_dataset_map("genres", is_static=True)
            genres_map_bool = load_dataset_map("genres", is_bool=True, is_static=True)
            #Conver the user input to list bool like for the knn model.
            genres_input = input_to_map(model_data["submission_genre"], genres_map, is_bool=True)
            #Get the most similar boolean list to what the user entered from those in the boolean map file
            #and set the input to be the genre of that list.
            genres_input = get_closest_map(genres_input, genres_map_bool)
            genres_input = np.array(genres_input, dtype=int)
            genres_input = genres_input.reshape(1, -1)
            genres_output = genre_model.predict(X=genres_input)
            #Age model
            #The same for the knn model, except age input is the index
            #of the entered value as it appears in the map file instead of being a binary list.
            age_map = load_dataset_map("movie_rated", is_static=True)
            age_input = input_to_map(model_data["submission_age"].lower(), age_map)
            age_input = np.array(age_input, dtype=int)
            age_input = age_input.reshape(1, -1)
            age_output = age_model.predict(X=age_input)
            #Date model
            #Same as knn model.
            date_input = int(model_data["submission_month"]) - 1
            date_input = np.array(date_input, dtype=int)
            date_input = date_input.reshape(1, -1)
            date_output = date_model.predict(X=date_input)
            #Runtime
            #Same as knn model.
            runtime_input = int(model_data["submission_runtime"])
            runtime_input = np.array(runtime_input, dtype=int)
            runtime_input = runtime_input.reshape(1, -1)
            runtime_output = runtime_model.predict(X=runtime_input)
            #Average outputs
            #Same as knn model.
            final_output = genres_output + age_output + date_output + runtime_output
            final_output = final_output / 4
            return str(round(final_output[0], 2))
    except Exception as e:
        error_exit(e, skip=True)
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