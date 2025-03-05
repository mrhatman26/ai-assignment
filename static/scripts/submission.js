console.log("submission.js loaded");
let form = document.getElementById("submission_form");
//Get the form used in submit.html.
//Then, using the form, get the HTML elements needed from the form.
let submit_button = form[7];
//Genre variables
let genre_select = form[0];
let genre_add = form[1];
let genre_clear = form[2];
let selected_genres = document.getElementById("selected_genres");
let selected_genres_array = [];
let genres_original_vals = [];
//Create a list of the original genres values.
for (var i = 0; i < genre_select.length; i++){
    genres_original_vals.push(genre_select[i].value);
}

//Other variables
let age_select = form[3];
let month_select = form[4];
let runtime_select = form[5];
let model_select = form[6];

//Genres Functions
function addGenre(event){
    //Take the currently selected genre, add it to selected_genres_array, make this addition visible to the user, then remove it from the select element.
    event.preventDefault();
    selected_genres_array.push(genre_select.value);
    selected_genres.innerHTML = "";
    for (var i = 0; i < selected_genres_array.length; i++){
        //Add the newly selected genre to the seleected_genres HTML element.
        //If it is empty, add the new genre with "Selected: " in front of it.
        //Else, the already added values and a comma in front of it.
        if (selected_genres.innerHTML === ""){
            selected_genres.innerHTML = "Selected: " + selected_genres_array[i];
        }
        else{
            selected_genres.innerHTML = selected_genres.innerHTML + ", " + selected_genres_array[i];
        }
    }
    //Remove the selected genre from the select element.
    genre_select.remove(genre_select.selectedIndex);
}

function clearGenres(event){
    //Reset the selected options back to default.
    //Seems a bit buggy?
    event.preventDefault();
    //Reset selected genres array to nothing.
    selected_genres_array = [];
    selected_genres.innerHTML = "Selected: None";
    //Remove all options from select.
    for (var i = 0; i < genre_select.length; i++){
        genre_select.remove(i);
    }
    //Add original options back to select.
    for (var i = 0; i < genres_original_vals.length; i++){
        var option = document.createElement("option");
        option.value = genres_original_vals[i];
        option.innerHTML = genres_original_vals[i];
        genre_select.appendChild(option);
    }
}

//Misc functions
function toInt(value){
    //Attempts to convert a string to an integer.
    //If successfull, it returns the integer, else it returns null.
    if (!isNaN(value)){
        return parseInt(value);
    }
    else{
        return null;
    }
}

//Submit function
function submit_data(event){
    //Takes the entered data, confirms nothing is missing and that the minutes are a number, then
    //sends this data to Python Flask using the POST method on the "/predict/validate/" URL.
    event.preventDefault();
    if (selected_genres_array.length < 1){
        //If the user has not selected at least one genre, show an error.
        var error_message = document.createElement("p");
        error_message.innerHTML = "Please select atleast one genre.";
        error_message.style.color = "red";
        document.getElementById("page_header").appendChild(error_message).scrollTo();
        return;
    }
    if (runtime_select.value == ""){
        //If no runtime value has been entered, show an error.
        var error_message = document.createElement("p");
        error_message.innerHTML = "Please enter a runtime.";
        error_message.style.color = "red";
        document.getElementById("page_header").appendChild(error_message).scrollTo();
        return;
    }
    if (toInt(runtime_select.value) === null){
        //If the runtime value cannot be converted into an intger, show an error.
        var error_message = document.createElement("p");
        error_message.innerHTML = "Runtime must be a whole number.";
        error_message.style.color = "red";
        document.getElementById("page_header").appendChild(error_message).scrollTo();
        return;
    }
    if (toInt(runtime_select.value) < 1){
        var error_message = document.createElement("p");
        error_message.innerHTML = "Runtime must be a valid number.";
        error_message.style.color = "red";
        document.getElementById("page_header").appendChild(error_message).scrollTo();
        return;
    }
    //Convert the entered data to a dictionary.
    var submission_data = {
        "submission_genre": selected_genres_array,
        "submission_age": age_select.value,
        "submission_month": month_select.value,
        "submission_runtime": toInt(runtime_select.value),
        "submission_model": model_select.value
    };
    //Send the data to Flask using the POST method.
    $.ajax({
        type: "POST",
        url: "/predict/validate/",
        data: JSON.stringify(submission_data),
        error: function(){
            //If not response is given in 10 seconds, show an error message.
            var error_message = document.createElement("p");
            error_message.innerHTML = "The server took too long to respond. \nPlease try again.";
            error_message.style.color = "red";
            document.getElementById("page_header").appendChild(error_message).scrollTo();
        },
        success: function(response){
            //Upon response.
            if (response === "failed"){
                //If the response is "failed", show an error message.
                var error_message = document.createElement("p");
                error_message.innerHTML = "An error occurred when predicting your movie's user rating.\nPlease try again.";
                error_message.style.color = "red";
                document.getElementById("page_header").appendChild(error_message).scrollTo();
            }
            else{
                //Else, redirect the user to the output page along with the response given.
                window.location.replace("/predict/output/output=" + response);
            }
        },
        timeout: 10000 //Flask has 10 seconds to respond before the response is timed out.
    })
}

//Genres Event Listeners
//Add event listeners to all of the buttons to link them to their corresponding functions.
genre_add.addEventListener("click", addGenre);
genre_clear.addEventListener("click", clearGenres);
submit_button.addEventListener("click", submit_data)