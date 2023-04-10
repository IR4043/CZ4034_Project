import joblib


def predict_sentiment(model_path, text):
    # Load the saved model
    model = joblib.load(model_path)
    # Predict the sentiment of the given text
    sentiment = model.predict([text])[0]
    # Return the predicted sentiment
    return sentiment


def process_data_for_analysis(dataframe):
    text = dataframe["text"]
    sentiment_result = []
    for row in text:
        sentiment = predict_sentiment("ensemble.pkl", row)
        if sentiment == 1:
            sentiment_result.append("Positive")
        else:
            sentiment_result.append("Negative")

    return sentiment_result


if __name__ == "__main__":
    model_path = "ensemble.pkl"
    text = "This is a positive review!"

    sentiment = predict_sentiment(model_path, text)

    print(sentiment)
