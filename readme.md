A program that creates eight machine learning models to predict an IMDb user rating of a potential movie.

To create the models, simply run "main.py".
This will create a new directory called "saved_data" where the graphs
and models will be saved to.

Once this has finished, you can predict a potentail move's user rating by launching the webapp through app.py.
This will launch a website on your localhost that will first copy the models from saved_data to the static folder.
Once this is done, you can go to the localhost and use the models from there.

Note: The website will most likely be broken if you try to run it without first creating the models, so don't do that.