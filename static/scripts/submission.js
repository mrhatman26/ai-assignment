console.log("submission.js loaded");
let form = document.getElementById("submission_form");
let submit_button = form[7];
//Genre variables
let genre_select = form[0];
let genre_add = form[1];
let genre_clear = form[2];
let selected_genres = document.getElementById("selected_genres");
let selected_genres_array = [];
let genres_original_vals = [];
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
    event.preventDefault();
    selected_genres_array.push(genre_select.value);
    selected_genres.innerHTML = "";
    for (var i = 0; i < selected_genres_array.length; i++){
        if (selected_genres.innerHTML === ""){
            selected_genres.innerHTML = "Selected: " + selected_genres_array[i];
        }
        else{
            selected_genres.innerHTML = selected_genres.innerHTML + ", " + selected_genres_array[i];
        }
    }
    genre_select.remove(genre_select.selectedIndex);
}

function clearGenres(event){
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
    if (!isNaN(value)){
        return parseInt(value);
    }
    else{
        return null;
    }
}

//Submit function
function submit_data(event){
    event.preventDefault();
    if (selected_genres_array.length < 1){
        var error_message = document.createElement("p");
        error_message.innerHTML = "Please select atleast one genre.";
        error_message.style.color = "red";
        document.getElementById("page_header").appendChild(error_message).scrollTo();
        return;
    }
    if (runtime_select.value == ""){
        var error_message = document.createElement("p");
        error_message.innerHTML = "Please enter a runtime.";
        error_message.style.color = "red";
        document.getElementById("page_header").appendChild(error_message).scrollTo();
        return;
    }
    if (toInt(runtime_select.value) === null){
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
    var submission_data = {
        "submission_genre": selected_genres_array,
        "submission_age": age_select.value,
        "submission_month": month_select.value,
        "submission_runtime": toInt(runtime_select.value),
        "submission_model": model_select.value
    };
    $.ajax({
        type: "POST",
        url: "/predict/validate/",
        data: JSON.stringify(submission_data),
        success: function(response){
            console.log(response);
        }
    })
}

//Genres Event Listeners
genre_add.addEventListener("click", addGenre);
genre_clear.addEventListener("click", clearGenres);
submit_button.addEventListener("click", submit_data)