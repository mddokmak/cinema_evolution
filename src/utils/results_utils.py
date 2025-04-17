import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# function to print the size of the dataframe
def print_df_size(name, df):
    print(name, f"- shape: {df.shape} --> {df.shape[0]} rows and {df.shape[1]} columns")

# We don't have information about inflation before 1913, so we will apply the 1913 inflation rates to the oldest movies
def inflation_date_constraint(date):
    if date.year<1913:
        return pd.Timestamp('1913-01-01')
    return date

# Function to clean the data after the merge of CMU Movie Summary Corpus with TMDB
def merge_cmu_tmdb_clean_columns(df_merged):
    """
    Cleans the merged DataFrame by dropping unnecessary columns.
    This function takes a merged DataFrame containing data from CMU and TMDB,
    and removes a predefined list of columns that are not needed for further analysis.
    
    Parameters :
        df_merged (pd.DataFrame) : 
            The merged DataFrame containing data from CMU and TMDB.
    Returns :
        pd.DataFrame : 
            A DataFrame with the specified columns removed.
    """
    
    columns_to_drop = [
    "wikipedia_movie_id",
    "movie_runtime",
    "movie_languages",
    "title",
    "status",
    "runtime",
    "adult",
    "backdrop_path",
    "budget",
    "homepage",
    "original_language",
    "original_title",
    "overview",
    "poster_path",
    "tagline",
    "production_companies",
    "spoken_languages",
    "keywords",
    "freebase_id",
    "id",
    "imdb_id"]
    full_reduced = df_merged.drop(columns=columns_to_drop)
    return full_reduced

# Function to remove dictionaries from the columns
def merge_cmu_tmdb_remove_dictionaries(full_reduced):
    """
    Cleans and merges movie country and genre information from different sources in the given DataFrame.
    This function performs the following steps:
    1. Cleans the 'movie_countries' and 'movie_genres' columns by evaluating their string representations of dictionaries
       and extracting their values.
    2. Converts the cleaned lists into comma-separated strings, replacing empty lists with NaN.
    3. Combines the cleaned 'movie_countries' and 'movie_genres' columns with 'production_countries' and 'genres' columns,
       respectively, prioritizing the cleaned columns.
    4. Drops the original and intermediate columns used in the cleaning process.
    
    Parameters :
        full_reduced (pd.DataFrame) : 
            A DataFrame containing movie information with columns 'movie_countries', 'movie_genres', 'production_countries', and 'genres'.
    Returns :
        pd.DataFrame : 
            The modified DataFrame with cleaned and merged movie country and genre information.
    """
    
    full_reduced["movie_countries_cleaned"] = full_reduced["movie_countries"].apply(lambda x: list(dict(eval(x)).values()))
    full_reduced["movie_genres_cleaned"] = full_reduced["movie_genres"].apply(lambda x: list(dict(eval(x)).values()))
    full_reduced["movie_countries_cleaned"] = full_reduced["movie_countries_cleaned"].apply(lambda x: np.nan if x == [] else ', '.join(map(str, x)) if isinstance(x, list) else x)
    full_reduced["movie_genres_cleaned"] = full_reduced["movie_genres_cleaned"].apply(lambda x: np.nan if x == [] else ', '.join(map(str, x)) if isinstance(x, list) else x)
    # Combining and dropping the original columns
    full_reduced['movie_countries_final'] = full_reduced['movie_countries_cleaned'].combine_first(full_reduced['production_countries'])
    full_reduced['movie_genres_final'] = full_reduced['movie_genres_cleaned'].combine_first(full_reduced['genres'])
    columns_to_drop = ['movie_countries_cleaned', 'production_countries', "movie_countries", 'movie_genres_cleaned', 'movie_genres', 'genres']
    full_reduced.drop(columns=columns_to_drop, inplace=True)
    return full_reduced

# Combine the redundant columns and ensure that we keep the maximum amount of information
def merge_cmu_tmdb_combine_columns(full_reduced):
    """
    Merges and combines specific columns in the given DataFrame.
    This function performs the following operations:
    1. Combines 'release_date' and 'movie_release_date' columns into a new column 'combined_release_date'.
    2. Drops the original 'release_date' and 'movie_release_date' columns.
    3. Converts 'combined_release_date' to datetime format, coercing errors.
    4. Replaces zero values in 'movie_box_office_revenue' and 'revenue' columns with NaN.
    5. Combines 'movie_box_office_revenue' and 'revenue' columns into a new column 'Box_Office'.
    6. Drops the original 'movie_box_office_revenue', 'revenue', 'movie_box_office_revenue_nan', and 'revenue_nan' columns.
    
    Parameters:
        full_reduced (pd.DataFrame) : 
            The DataFrame containing the columns to be merged and combined.
    Returns:
        pd.DataFrame : 
            The modified DataFrame with combined columns.
    """
    
    full_reduced['combined_release_date'] = full_reduced['release_date'].combine_first(full_reduced['movie_release_date'])
    full_reduced.drop(columns=['movie_release_date', 'release_date'], inplace=True)
    full_reduced['combined_release_date'] = pd.to_datetime(full_reduced['combined_release_date'], errors='coerce')
    full_reduced["movie_box_office_revenue_nan"]=full_reduced["movie_box_office_revenue"].replace(0, np.nan)
    full_reduced["revenue_nan"]= full_reduced["revenue"].replace(0, np.nan)
    full_reduced["Box_Office"] = full_reduced["movie_box_office_revenue_nan"].combine_first(full_reduced["revenue_nan"])
    full_reduced.drop(columns=['movie_box_office_revenue', 'revenue', "movie_box_office_revenue_nan", "revenue_nan"], inplace=True)
    return full_reduced

def combine_ratings(data_box_office):
    """
    Combines and processes rating columns in the given DataFrame.
    This function takes a DataFrame containing box office data with columns 'avgRating' and 'vote_avg'.
    It combines these columns to create a new rating column, 'rating', which is the average of the two.
    Missing values in 'avgRating' and 'vote_avg' are handled by filling them with zeros.
    
    Parameters:
        data_box_office (pd.DataFrame) : 
            A DataFrame containing box office data with 'avgRating' and 'vote_avg' columns.
    Returns:
        pd.DataFrame : 
            The modified DataFrame with a new 'rating' column and without the original 'avgRating' and 'vote_avg' columns.
    """
    
    data_box_office['avgRating_safe'] = data_box_office['avgRating'].combine_first(data_box_office['vote_avg'])
    data_box_office['vote_safe'] = data_box_office['vote_avg'].combine_first(data_box_office['avgRating'])
    data_box_office['avgRating_safe'].fillna(0, inplace=True)
    data_box_office['vote_safe'].fillna(0, inplace=True)
    data_box_office['rating'] = 0.5 * (data_box_office['avgRating_safe'] + data_box_office['vote_safe'])
    data_box_office.drop(columns=['avgRating', 'vote_avg', 'avgRating_safe', 'vote_safe'], inplace=True)
    return data_box_office

def success(data_box_office, popularity, box_office, sa_score, rating):
    """
    Calculate the success score for movies based on various metrics and scales it between 0 and 5.
    
    Parameters:
        data_box_office (pd.DataFrame) : 
            DataFrame containing movie data including box office information.
        popularity (str) : 
            Column name in data_box_office representing the popularity metric.
        box_office (str) : 
            Column name in data_box_office representing the box office metric.
        sa_score (str) : 
            Column name in data_box_office representing the sentiment analysis score.
        rating (str) : 
            Column name in data_box_office representing the movie rating.
    Returns:
        pd.DataFrame : 
            DataFrame with additional columns 'success_score' and 'success_metric_scaled', 
            sorted by 'success_metric_scaled' in descending order.
    """

    weights = {
        popularity: 10,
        box_office: 8,
        sa_score: 3,
        rating: 3
    }
    data_box_office['success_score'] = data_box_office.apply(
        lambda row: sum(row[col] * weight for col, weight in weights.items()), axis=1)
    # Just a scaling if we want our metric between 0 and 5 like regulare movie ratings

    # Initialize the MinMaxScaler to scale between 0 and 5
    scaler = MinMaxScaler(feature_range=(0, 5))

    # Fit and transform the Success_metric column
    data_box_office['success_metric_scaled'] = scaler.fit_transform(data_box_office[['success_score']])
    data_box_office = data_box_office.sort_values(by='success_metric_scaled', ascending=False)
    return data_box_office

def get_decade(year):
    return (year // 10) * 10
