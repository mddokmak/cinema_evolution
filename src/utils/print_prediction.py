import matplotlib.pyplot as plt

def plot_results(train, test, predicted_values, title):
    """
    Plots the training data, test data, and predicted values on a single graph.

    train : list or array-like
        The training data values.
    test : list or array-like
        The test data values.
    predicted_values : list or array-like
        The predicted values to be plotted.
    title : str
        The title of the plot.

    Returns None
    """
    plt.figure(figsize=(10, 5))

    plt.plot(range(len(train)), train, label='Train Data')

    plt.plot(range(len(train), len(train) + len(test)), test, label='Test Data')

    prediction_range = range(len(train), len(train) + len(predicted_values))
    plt.plot(prediction_range, predicted_values, label='Predicted', linestyle='--')

    plt.title(title)
    plt.legend()
    plt.show()
