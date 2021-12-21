import pytest

from americanhandelsociety_app.newsletters import NewslettersData


@pytest.mark.parametrize(
    "filename,expected_season,expected_year",
    [
        ("Winter_1987.pdf", "Winter", "1987"),
        ("Spring_2009No.1.pdf", "Spring", "2009"),
        ("HandelNewsletter_winter_2012.pdf", "winter", "2012"),
        ("AHS_Newsletter_Summer_2011.pdf", "Summer", "2011"),
    ],
)
def test_get_newsletter_season_and_year(filename, expected_season, expected_year):
    season, year = NewslettersData.get_newsletter_season_and_year(filename)

    assert season == expected_season
    assert year == expected_year


def test_friendly_name_with_label_preview():
    result = NewslettersData(
        directory_path="newsletters/previews"
    ).friendly_name_with_label("Summer 1785")

    assert result == 'Summer 1785<br><span class="preview-label">Preview</span>'


def test_friendly_name_with_label_members_only():
    result = NewslettersData(
        directory_path="newsletters/members_only"
    ).friendly_name_with_label("Summer 1785")

    assert (
        result == 'Summer 1785<br><span class="members-only-label">Members Only</span>'
    )


def test_friendly_name_with_label_no_label():
    result = NewslettersData(directory_path="newsletters").friendly_name_with_label(
        "Summer 1785"
    )

    assert result == "Summer 1785"


def test_generate_newsletters_data():
    pass
