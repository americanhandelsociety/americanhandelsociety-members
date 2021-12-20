import re

# TODO:
# 1. tests!
# 2. include hash map for articles
# 3. how can this be more efficient? where can I cache?
# 4. how to deal with "previews" and "member" views?


class NewslettersData:
    def __init__(self, newsletter_filenames):
        self.newsletter_filenames = newsletter_filenames

    def _get_newsletter_season_and_year(self, filename):
        pattern = r"([a-zA-Z]{6})_(\d{4})"
        m = re.search(pattern, filename)
        season = m.group(1)
        year = m.group(2)

        return season, year

    def generate_newsletters_data(self):
        newsletters_data = []

        for filename in self.newsletter_filenames:
            data = {}

            season, year = self._get_newsletter_season_and_year(filename)
            data["id"] = f"{year}_{season}".lower()
            data["friendly_name"] = f"{season} {year}".title()
            data["filename"] = f"newsletters/{filename}"

            newsletters_data.append(data)

        return newsletters_data
