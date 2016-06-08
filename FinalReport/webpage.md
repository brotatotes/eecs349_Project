# Project Title
Project Members: Eric Hao, Dylan Ong, Max Schuman, Siyu Zhang  
Contact Email: [erichao2018@u.northwestern.edu](erichao2018@u.northwestern.edu)  
Northwestern University: Spring 2016 EECS 349 Machine Learning  
## Introduction
Our task is not only to predict the winner of the 2017 GRAMMY Record of the Year award, but also to
present the songs most likely to be nominated for the award. Because our model can be easily applied to
future GRAMMY seasons, these results will yield insights into subtle differences between popular
expectations and actual winners, especially in upset years, and can help provide context for identifying
shifts and trends in popular music. The output of our project is a rank of songs based on their probabilities
to win the GRAMMY Award, given a list of the current top 100 songs eligible for the award and their
relevant attributes.
## Our Model
We used a multilayer perceptron model with two hidden layers to make our predictions, which computed
the predicted winner score for each song. (In the data, winner_score is 1 if a song won and 0.2 if a song
was nominated but did not win). Then, we ranked every song in each year by its winner score to evaluate
our predictions. In order to take the fleeting fashion trend into consideration, we assigned each song an
associated weight based on its year so that songs from recent years can have more significance when we
predicted the winner and nominees for 2017. For each song, we considered 23 attributes, 5 of which are
nominal and 19 of which are numeric. 4 nominal attributes are: year, genre, key, mode, time_signature.
19 numeric attributes are: popularity, danceability, energy, loudness, speechiness, acousticness,
instrumentalness, liveness, valence, tempo, duration_ms, word_count, reading_ease, polarity, subjectivity,
followers, listeners, play_count.
## Scraping, Testing, and Training
We scrapped data from Spotify and Last.fm to obtain various attributes. The data set we have compiled
includes roughly 5400 songs from 1958 to 2015. All of these songs were part of the Billboard Year-End
Top 100 List. There are 4955 songs from 1958 to 2015 used as training set and 450 songs from 2010 to
2015 used as validation set. We applied the following equation to set up the weight of each data entry
based on the year of release.
![Image of Equation](https://github.com/brotatotes/eecs349_Project/FinalReport/eqn.gif)  
The validation result is satisfiable.
## Results