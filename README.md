
## Needed Packages

To run the Watson Tone Analyzer, you will need to download the watson module:

```
$ pip install --upgrade watson-developer-cloud
```

Then you will need to make an [IBM Bluemix](https://console.ng.bluemix.net/) account.

To run the Grammar Check, you will need to download the module:

```
$ pip install grammar_check
```

All of our training and testing data have the watson tone analysis and grammatical error count included, so this step is not necessary to view the project notebook and/or create classifiers using the subreddit specific notebooks.

However, if you do wish to run the django webserver, you will need to follow the above instructions as well as replace the `user` and `password` strings found on line 316 of `webapp/api/views.py` to reflect the values given to you by IBM.

```python
df = mg.munge_dataset(df, badwords, 'user', 'password')
```

## Initial Data

We pulled our [training](https://github.com/jsmoorman/csce489_gold/tree/master/Subreddits/mytrain) and [testing](https://github.com/jsmoorman/csce489_gold/tree/master/Subreddits/mytest) datasets from the top-level comments of 2015 in this [complete dataset](https://archive.org/download/2015_reddit_comments_corpus).

We limited our scope to the newest data (2015) since the files were so large (>30GB) and since we had limited IBM Watson requests.  We also only analyzed top-level comments since they require the least context to be relevant.

## Creating Classifiers

To create a classifier for each subreddit, simply run the corresponding notebook found [here](https://github.com/jsmoorman/csce489_gold/tree/master/Subreddits).

Each note book consists of 2 parts.

1. Running a recursive feature exclusion to find the best features for this subreddit given the training and testing data.

2. Using given features (defaulted to use those from the feature exclusion) to build a classifier.

These classifiers are exported and saved after they are created and ready to be imported into the webapp.

## Running the Django Server and Webpage

To run the django server, you will need to download the source code from the [webapp](https://github.com/jsmoorman/csce489_gold/tree/webapp) branch and host the application using your choice of software (apache, uwsgi, etc.).  Upload any of your modified classifiers made in the previous step into the `webapp/api/classifiers/` folder and overwrite the existing ones.

__Note:__ Make sure to change the array of features in the corresponding function for the subreddit in `webapp/api/views.py` or the classifier will be trying to compare the incorrect features from your input.

Now your application is ready to accept input and return its prediction.

To create a webpage that sends requests to your server, download the [gh-pages](https://github.com/jsmoorman/csce489_gold/tree/gh-pages/) branch of the repository, change line 44 of `js/scripts.js` to point to your hosted django server, and host the page however you see fit.

## Video

Our 2 minute video showcasing the website can be found [here](https://youtu.be/8thl64JJR0Y).

## Project Website

Our final project website can be found [here](https://jsmoorman.github.io/csce489_gold/).