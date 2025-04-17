# ADA 2024 - Gear 5: Evolution of cinema through the years, finding the golden age

**Project Mentor:** [Shuo Wen](http://personnes.epfl.ch/shuo.wen) ([Email](shuo.wen@epfl.ch))  
**Authors:** Mahmoud Dokmak, Matthieu Borello, Léo Brunneau, Loïc Domingos, Bastien Armstrong  

<hr style="clear:both">

## Website

You can find the project website [here](https://loxpac.github.io/).

## Quickstart

```bash
# clone project
git clone https://github.com/epfl-ada/ada-2024-project-gear5.git
cd <project repo>

# [OPTIONAL] create conda environment
conda create -n <env_name> python=3.12
conda activate <env_name>

# install requirements
pip install -r pip_requirements.txt
```

## Abstract

This project delves into the evolution of cinema to explore whether a “Golden Age” has existed and to identify the key factors that define success across eras. By analyzing historical and contemporary trends in film production, genre popularity, and global appeal, we aim to uncover patterns that reflect shifts in cinematic influence and cultural resonance over time. Our approach considers both the artistic and economic dimensions of the film industry, examining how certain genres, themes, and regions rise to prominence and shape cinematic eras. Ultimately, we seek to understand where the current landscape fits within cinema’s broader history and what trends may lie ahead. Through data-driven insights, we hope to tell a compelling story of cinema’s dynamic journey and its role in reflecting and shaping society across decades.

## Research questions

1. Has there ever been a "Golden Age" of cinema ? Which metrics are important to evaluate the global success of the cinema industry and, therefore, a potential "Golden Age" ?

2. What were the specific ages of cinema throughout the years ? Is it possible to observe time-related trends about a specific genre or country ?

3. What about now ? Are we in a specific era ? What are the past decade trends and what could we infer from this ? Can we build a strong metric that predicts a future trend and, therefore, a movie success ?

## Additional datasets
In addition to the original dataset [CMU Movie Summary Corpus](http://www.cs.cmu.edu/~ark/personas/), we are using the [MovieLens Tag Genome Dataset 2021](https://grouplens.org/datasets/movielens/)  and [Full TMDB Movies Dataset 2024](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies/data) datasets.
The[MovieLens Tag Genome Dataset 2021](https://grouplens.org/datasets/movielens/) dataset gives us access to reviews and ratings for a wide range of movies.
The TMBb dataset allows us to enrich our original dataset by offering a dataset that is closer in style to the original [CMU Movie Summary Corpus](http://www.cs.cmu.edu/~ark/personas/) one.

## Methods

### Part 1 - Defining the "Golden Age" thanks to the success metric

For our project, we intend on defining the relative success of a movie by assessing multiple statistics. These metrics include:

- The popularity of a movie: We get a popularity score from the TMDb dataset, which is a metric that takes into account the following:
  - Release date
  - Number of users who added it to their "watchlist" for the day
  - Number of users who marked it as a "favourite" for the day
  - Number of views for the day
  - Number of votes for the day
  - Total number of votes
  - Vote average
  - Previous day's popularity score
- The box office revenue of a movie adjusted for inflation. One can identify the "Golden Age" based on financial success by pointing out the period when the cinema industry generated the most revenue adjusted to inflation.
- User movie ratings (from [MovieLens Tag Genome Dataset 2021](https://grouplens.org/datasets/movielens/)). This metric gives the grade given by individual users on the MovieLens website. Viewers opinions are important to assess the success of a movie.
- Reviews sentiment analysis (from [MovieLens Tag Genome Dataset 2021](https://grouplens.org/datasets/movielens/)) dataset: We run sentiment analysis on reviews, defining if they are positive or negative, and thus assess the again the viewers' point of view. For the sentiment analysis, we use a pretrained Bert model and a pretrained tokenizer available on HugginFace [here](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english).

We define the "Golden Age" per genre as the decade where the average success score is the highest. This will allow us to identify the most successful genres and periods in cinema history.

### Part 2 - Time-related trends analysis per genre and country

Once the robust success metric is created, we want to apply it to all the movies in our combined dataset. This will help us to indicate how movie success (measured by popularity, box office, ratings, and sentiment) changes over time by genre, helping to identify shifts in dominant genres and regions, and pinpoint key cinematic "eras."
The data will be preprocessed by grouping movies based on their genres (handling multi-genre films) and countries of origin. Then, we will calculate success metrics for each movie, aggregated by year, genre, and country.
Using these metrics, we will create time-series data to track the success of different genres and countries over time. For each group, we will calculate the average success score, total box office revenue (adjusted for inflation), and the number of films produced.
These trends will be analyzed in order to identify which genres and countries have been most successful at different times. For example, we might see action films rise in the 1980s or how Bollywood’s global influence grew in the 2000s. We’ll also look for cultural patterns, like the dominance of war films during WWII.
To visualize these trends, we can use line charts for success scores, stacked bar charts for film production by genre or country, and heatmaps for sentiment analysis over time. This will help us identify key shifts in genre and country dominance.
This analysis will allow us to define cinematic "eras" based on dominant genres or countries, such as the Golden Age of Hollywood or the rise of global cinema in the 21st century.

### Part 3 - What about now ?

Here, our goal is to compile all the information from our success metric into time-series to make predictions. Our objective is to then use predictive models on these time-series to evalute the future state of the movie industry. We have chosen to use the ARIMA (Autoregressive Integrated Moving Average) model and we are going to compare it's predictions against a simple 2nd order polynomial regression. Some further details into the reasons for this choice and into how we applied these methods are available in the `methods.ipynb` notebook. 
Our plan is to first show that the impact time-series (that take as input the success metric) work well. We have set two conditions that we wanted to respect when creating these series for them to be meaningful:
- More success = More impact. This makes sense, but we truely wanted high success movie to have a vastly greater impact and low success movies to have a nearly negligible impact.
- Causality. We did not want the success of the movie to have an impact before before it's release date. This disqualified algorithms such as gaussian kernel regression from contention. 

NB: Once again, more details on the methods we used to achieve this are available in the `methods.ipynb` notebook.

We are then going to compare the prediction results we obtain from the two models we have chosen. We expect the polynomial regression to perform worse as it's a "simplistic" prediction, but it can serve as a sort of baseline to judge the results of the ARIMA model.

Finally, we are going to reveal the movie genre which will according to us have the most impact of the industry in future years.



## Project timeline

Week 9 -- 11/11 - 17/11:

- [x] Finding the additional datasets needed for the idea
- [x] Combining the dataset and cleaning the data
- [x] Have Proofs of concepts for all the methods we want to use in the project
- [x] Project P2 deadline

Week 10 -- 18/11 - 24/11:

- [x] Running the sentiment analysis on the movie critics: **Mahmoud**, **Matthieu**
- [x] Defining the "success" metric and testing it on selected movies to see how well it works: **Loïc**, **Léo**, **Bastien**

Week 11 -- 25/11 - 01/12:

- [x] Finish the first part of the project
- [x] Success yearly arrays analysis to find "golden ages": **Léo**, **Matthieu**, **Bastien**
- [x] Vizualisation of the results found: **Loïc**, **Mahmoud**

Week 12 -- 02/12 - 08/12:

- [x] Data vizualisation for second part: **Mahmoud**, **Bastien**
- [x] Using predictive models on the success yearly arrays for part 3: **Léo**, **Loïc**, **Matthieu**

Week 13 -- 09/12 - 15/12:

- [x] Start writing the story. Will need to complete work done with more vizualisations: **Léo**, **Loïc**, **Mahmoud**

Week 14 -- 16/12 - 20/12:

- [x] Project P3 deadline
- [x] Finish the story we want to tell: **Bastien**, **Matthieu**

## Team organization

- Matthieu: Success Metric definition, Predictive Models (ARIMA)
- Mahmoud: Data Wrangling, Sentiment Analysis, Success Metric definition
- Bastien: Datastory writing, Data Visualization
- Léo: Data Visualization, Data Wrangling
- Loïc: Data Visualization, Website Optimization, Datastory writing

## Project Structure

The directory structure of new project looks like this:

```text
├── data                        <- Project data files
│   │
│   ├── CMU_movie                       <- Original CMU movies dataset
│   ├── Converter                       <- Converter dataset used to match movie IDs
│   ├── MovieLens                       <- MovieLens dataset with ratings and reviews
│   ├── MovieSummaries                  <- Movie Summaries
│   └── TMDBMovies                      <- TMDB Movies dataset to enrich the original dataset
│
├── plots                       <- Our html plots
├── src                         <- Source code
│   ├── models    
│   │   │
│   │   ├── ARIMA.py                        <- Used to run the ARIMA algo
│   │   ├── PolynomialRegression.py         <- Used to run the polynomial regression 
│   │   ├── Impact.py                       <- Used to calculate impact of a given genre
│   │   └── sentiment_analysis.py           <- Used to calculate impact of a given genre
│   │  
│   └── utils                           <- Utility directory
│       │
│       ├── print_prediction.py             <- Printing prediction proof of concept
│       └── result_utils.py                 <- Utilities
│
├── .gitignore                  <- List of files ignored by git
├── requirements.txt            <- File for installing python dependencies
├── data.ipynb                  <-  a well-structured notebook used to load and preprocess the data
├── methods.ipynb               <- a well-structured notebook showing the methods used
├── result.ipynb                <- a well-structured notebook showing our results
├── resultsM2.ipynb             <- a well-structured notebook showing our results for milestone 2
├── sentiment_analysis.ipynb    <- a well-structured notebook to run sentiment analysis
├── READMEM2.md                 <- The Milestone 2 README.
└── README.md                   <- The top-level README for developers using this project.

```
