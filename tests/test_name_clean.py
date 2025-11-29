from app.models import PassengerClean

def test_title_normalize():
    from app.cleaning.name_clean import NameNormalizer

    name_normalizer = NameNormalizer()
    passager = name_normalizer.apply(
        PassengerClean(Name="Doe,  sir.   john", Age=30, Pclass=2, Fare=50.0, Title="Sir", Title_Normalized="Mr")
    )
    assert passager.Name == "Doe, Sir. John"