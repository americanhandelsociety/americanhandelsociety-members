from americanhandelsociety_app.models_utils import BaseTextChoices


def test_base_text_choices_max_length():
    class FakeTextChoices(BaseTextChoices):
        A = "A"
        AB = "AB"
        ABC = "ABC"

    assert FakeTextChoices.max_length() == 3
