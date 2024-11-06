"""
Note: These tests will fail if you have not first trained the model.
"""

import numpy as np
from sklearn.metrics import accuracy_score

from red_wine_mm.predict import make_prediction


def test_make_prediction(sample_input_data):
    x_test, y_test = sample_input_data
    # Given
    expected_no_predictions = 159

    # When
    result = make_prediction(input_data=x_test)

    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions, np.ndarray)
    assert isinstance(predictions[0], np.int64)
    assert result.get("errors") is None
    assert len(predictions) == expected_no_predictions
    _predictions = list(predictions)
    accuracy = accuracy_score(_predictions, y_test)
    print(f"accuracy score: {accuracy}")
    assert accuracy > 0.90
