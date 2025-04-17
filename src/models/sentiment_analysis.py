import pandas as pd
import torch
from tqdm import tqdm
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification


tqdm.pandas()

def sentiment_analysis(reviews, sa_column, item_id, index ,output_file):
    #ensure that the columns exist
    for column in [sa_column, item_id, index]:
        if column not in reviews.columns:
            raise ValueError(f"The column {column} doesn't exist")
    # Loading a Pre-Trained Model from HuggingFace Hub
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    print(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    #ensure that the reviews are not too long.
    reviews[sa_column] = [
        reviews[sa_column].iloc[i][:512] if isinstance(reviews[sa_column].iloc[i], str) else reviews[sa_column].iloc[i]
        for i in range(reviews.shape[0])
    ]
    #intialize the sentiment analysis classifier
    device = 0 if torch.cuda.is_available() else -1
    sa_classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=device)
    sa = apply_sentiment_analysis(sa_classifier, reviews, sa_column, item_id, index, output_file)
    return sa

def apply_sentiment_analysis(sa_classifier, reviews, sa_column, item_id, index, output_file):
    reviews["sentiment_analysis"] = reviews[sa_column].progress_apply(lambda x: sa_classifier(x)[0] if pd.notnull(x) else None)
    columns_to_keep = ["sentiment_analysis", item_id, index]
    reviews = reviews[columns_to_keep]
    reviews.to_csv(output_file, index=True)
    return reviews