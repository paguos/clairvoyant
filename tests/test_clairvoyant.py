import pytest

from clairvoyant import Clairvoyant

from datetime import date, timedelta


def generate_dates(start_date, number_of_days):
    return [start_date + timedelta(days=i) for i in range(number_of_days)]


@pytest.fixture
def mock_dataset():
    mock_data = {}
    mock_data["ds"] = generate_dates(date(2020, 1, 1), 150)

    for key in ["a", "b", "c"]:
        mock_data[key] = [i for i in range(0, 150)]

    return mock_data


def test_divide_dataset(mock_dataset):
    clairvoyant = Clairvoyant(mock_dataset, 0.75)

    assert len(list(clairvoyant.training_data.values())[0]) == 112
    assert len(list(clairvoyant.test_data.values())[0]) == 38

    expected_training = [i for i in range(0, 112)]
    expected_training_dates = generate_dates(date(2020, 1, 1), 112)
    for key in clairvoyant.training_data.keys():
        if "ds" == key:
            assert clairvoyant.training_data[key] == expected_training_dates
        else:
            assert clairvoyant.training_data[key] == expected_training

    expected_test = [i for i in range(112, 150)]
    expected_test_dates = generate_dates(date(2020, 4, 22), 38)
    for key in clairvoyant.test_data.keys():
        if "ds" == key:
            assert clairvoyant.test_data[key] == expected_test_dates
        else:
            assert clairvoyant.test_data[key] == expected_test


def test_invalid_dataset():
    empty_dataset = {}
    with pytest.raises(ValueError) as excinfo:
        Clairvoyant(empty_dataset, 0.75)
    assert "Dataset has not 'ds' key!" in str(excinfo.value)

    invalid_dataset = {"ds": generate_dates(date(2020, 1, 1), 5)}
    with pytest.raises(ValueError) as excinfo:
        Clairvoyant(invalid_dataset, 0.75)
    assert "Dataset must have at least 2 keys!" in str(excinfo.value)

    invalid_length_dataset = {
        "ds": generate_dates(date(2020, 1, 1), 5),
        "y": [0, 1]
    }
    with pytest.raises(ValueError) as excinfo:
        Clairvoyant(invalid_length_dataset, 0.75)
    assert "All columns/values need the same length!" in str(excinfo.value)


def test_invalid_training_ratio(mock_dataset):
    with pytest.raises(ValueError) as excinfo:
        Clairvoyant(mock_dataset, -1)
    assert "Training ratio must be between 0 and 1!" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        Clairvoyant(mock_dataset, 2)
    assert "Training ratio must be between 0 and 1!" in str(excinfo.value)
