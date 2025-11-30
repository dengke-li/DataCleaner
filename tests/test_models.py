import pytest


def test_passage_raw():
    from app.models import PassengerRaw

    # Valid data
    passenger = PassengerRaw(Name="Doe, Mr. John", Age=30, Pclass=2, Fare=50.0)
    assert passenger.Name == "Doe, Mr. John"
    assert passenger.Age == 30
    assert passenger.Pclass == 2
    assert passenger.Fare == 50.0

    # Invalid Name
    with pytest.raises(ValueError):
        PassengerRaw(Name="   ", Age=30, Pclass=2, Fare=50.0)

    # Invalid Age
    with pytest.raises(ValueError):
        PassengerRaw(Name="Doe, Mr. John", Age=-5, Pclass=2, Fare=50.0)

    # Invalid Pclass
    with pytest.raises(ValueError):
        PassengerRaw(Name="Doe, Mr. John", Age=30, Pclass=4, Fare=50.0)

    # Invalid Fare
    with pytest.raises(ValueError):
        PassengerRaw(Name="Doe, Mr. John", Age=30, Pclass=2, Fare=0)
