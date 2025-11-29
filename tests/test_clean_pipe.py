def test_clean_pipe():
    from app.cleaning.pipeline import titanic_cleaner
    from app.models import PassengerRaw

    passage_raw = PassengerRaw(Name="  doe,   lady.   jane  ", Age=28, Pclass=1, Fare=100.0)
    passenger = titanic_cleaner.run(passage_raw)

    assert passenger.Name == "Doe, Lady. Jane"
    assert passenger.Title == "lady"
    assert passenger.Title_Normalized == "Mrs"