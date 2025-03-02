console.log("submission.js loaded");
let form = document.getElementById("submission_form");
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

//Age Functions

//Date Functions

//Runtime functions
function toInt(value){
    if (!isNaN(value)){
        return parseInt(value);
    }
    else{
        return null;
    }
}

//Genres Event Listeners
genre_add.addEventListener("click", addGenre);
genre_clear.addEventListener("click", clearGenres);
console.log(toInt("50"));