import pytest

from app.models import PassengerClean

def test_title_extract():
    from app.cleaning.title_clean import TitleExtractor

    title_extractor = TitleExtractor()
    passager = title_extractor.apply(
        PassengerClean(Name="Doe, Sir. John", Age=30, Pclass=2, Fare=50.0, Title=None, Title_Normalized=None)
    )
    assert passager.Title == "Sir"

def test_title_normalize():
    from app.cleaning.title_clean import TitleNormalizer

    title_normalizer = TitleNormalizer()
    passager = title_normalizer.apply(
        PassengerClean(Name="Doe, Sir. John", Age=30, Pclass=2, Fare=50.0, Title="Sir", Title_Normalized=None)
    )
    assert passager.Title_Normalized == "Mr"

    passager = title_normalizer.apply(
        PassengerClean(Name="Doe, Lady. Jane", Age=30, Pclass=2, Fare=50.0, Title="Lady", Title_Normalized=None)
    )
    assert passager.Title_Normalized == "Mrs"

    passager = title_normalizer.apply(
        PassengerClean(Name="Doe, Dr. John", Age=30, Pclass=2, Fare=50.0, Title="Dr", Title_Normalized=None)
    )
    assert passager.Title_Normalized == "Rare"