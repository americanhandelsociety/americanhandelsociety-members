import os
import re

from django.conf import settings

# TODO:
# 1. tests!
# 2. include hash map for articles
# 4. how to deal with "previews" and "member" views?


class NewslettersData:
    def __init__(self):
        self.newsletter_filenames = os.listdir(
            os.path.join(settings.STATIC_ROOT, "newsletters")
        )

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
            data["filename"] = f"/newsletters/{filename}"

            newsletters_data.append(data)

        sorted_newsletters_data = sorted(
            newsletters_data, key=lambda x: x["id"], reverse=True
        )
        return sorted_newsletters_data


# This data was generated (locally) using NewslettersData.
# We do this locally, since Whitenoise (the static file server) and its compressed files
# makes it challenging to dynamically iterate over static files in a production environment.
NEWSLETTERS_DATA = [
    {
        "id": "2020_summer",
        "friendly_name": "Summer 2020",
        "filename": "/newsletters/Handel_Summer_2020.pdf",
    },
    {
        "id": "2020_spring",
        "friendly_name": "Spring 2020",
        "filename": "/newsletters/Handel_Spring_2020.pdf",
    },
    {
        "id": "2019_winter",
        "friendly_name": "Winter 2019",
        "filename": "/newsletters/Handel_Winter_2019.pdf",
    },
    {
        "id": "2019_summer",
        "friendly_name": "Summer 2019",
        "filename": "/newsletters/Handel_Summer_2019.pdf",
    },
    {
        "id": "2019_spring",
        "friendly_name": "Spring 2019",
        "filename": "/newsletters/Handel_Spring_2019.pdf",
    },
    {
        "id": "2018_winter",
        "friendly_name": "Winter 2018",
        "filename": "/newsletters/Handel_Winter_2018.pdf",
    },
    {
        "id": "2018_summer",
        "friendly_name": "Summer 2018",
        "filename": "/newsletters/Handel_Summer_2018_Web.pdf",
    },
    {
        "id": "2018_spring",
        "friendly_name": "Spring 2018",
        "filename": "/newsletters/Handel_Spring_2018.pdf",
    },
    {
        "id": "2017_winter",
        "friendly_name": "Winter 2017",
        "filename": "/newsletters/Handel_Winter_2017.pdf",
    },
    {
        "id": "2017_summer",
        "friendly_name": "Summer 2017",
        "filename": "/newsletters/Handel_Summer_2017.pdf",
    },
    {
        "id": "2017_spring",
        "friendly_name": "Spring 2017",
        "filename": "/newsletters/AHS Newsletter_Spring_2017_.pdf",
    },
    {
        "id": "2016_winter",
        "friendly_name": "Winter 2016",
        "filename": "/newsletters/Handel_Winter_2016_WEB.pdf",
    },
    {
        "id": "2016_summer",
        "friendly_name": "Summer 2016",
        "filename": "/newsletters/Handel_Summer_2016_WEB.pdf",
    },
    {
        "id": "2016_spring",
        "friendly_name": "Spring 2016",
        "filename": "/newsletters/Handel_Spring_2016_WEB.pdf",
    },
    {
        "id": "2015_winter",
        "friendly_name": "Winter 2015",
        "filename": "/newsletters/Handel_Winter_2015_WEB.pdf",
    },
    {
        "id": "2015_summer",
        "friendly_name": "Summer 2015",
        "filename": "/newsletters/Handel_Summer_2015_WEB (1).pdf",
    },
    {
        "id": "2015_spring",
        "friendly_name": "Spring 2015",
        "filename": "/newsletters/Handel_Spring_2015_WEB.pdf",
    },
    {
        "id": "2014_winter",
        "friendly_name": "Winter 2014",
        "filename": "/newsletters/Handel_Winter_2014_Web.pdf",
    },
    {
        "id": "2014_summer",
        "friendly_name": "Summer 2014",
        "filename": "/newsletters/Handel_Summer_2014_Web.pdf",
    },
    {
        "id": "2014_spring",
        "friendly_name": "Spring 2014",
        "filename": "/newsletters/Handel_Spring_2014_Web.pdf",
    },
    {
        "id": "2013_winter",
        "friendly_name": "Winter 2013",
        "filename": "/newsletters/AHS_Newsletter_Winter_2013.pdf",
    },
    {
        "id": "2013_summer",
        "friendly_name": "Summer 2013",
        "filename": "/newsletters/AHS_Newsletter_Summer_2013.pdf",
    },
    {
        "id": "2013_spring",
        "friendly_name": "Spring 2013",
        "filename": "/newsletters/AHS_Newsletter_Spring_2013.pdf",
    },
    {
        "id": "2012_winter",
        "friendly_name": "Winter 2012",
        "filename": "/newsletters/HandelNewsletter_Winter_2012.pdf",
    },
    {
        "id": "2012_summer",
        "friendly_name": "Summer 2012",
        "filename": "/newsletters/Handel_Summer_2012_Proof.pdf",
    },
    {
        "id": "2011_winter",
        "friendly_name": "Winter 2011",
        "filename": "/newsletters/AHSNewsletter_Winter_2011.pdf",
    },
    {
        "id": "2011_summer",
        "friendly_name": "Summer 2011",
        "filename": "/newsletters/AHSNewsletter_Summer_2011.pdf",
    },
    {
        "id": "2011_spring",
        "friendly_name": "Spring 2011",
        "filename": "/newsletters/AHSNewsletter_Spring_2011.pdf",
    },
    {
        "id": "2010_winter",
        "friendly_name": "Winter 2010",
        "filename": "/newsletters/Winter_2010.pdf",
    },
    {
        "id": "2010_summer",
        "friendly_name": "Summer 2010",
        "filename": "/newsletters/Summer_2010.pdf",
    },
    {
        "id": "2010_spring",
        "friendly_name": "Spring 2010",
        "filename": "/newsletters/Handel_Spring_2010_PROOF.pdf",
    },
    {
        "id": "2009_winter",
        "friendly_name": "Winter 2009",
        "filename": "/newsletters/Winter_2009.pdf",
    },
    {
        "id": "2009_summer",
        "friendly_name": "Summer 2009",
        "filename": "/newsletters/Summer_2009.pdf",
    },
    {
        "id": "2009_spring",
        "friendly_name": "Spring 2009",
        "filename": "/newsletters/Spring_2009No.1.pdf",
    },
    {
        "id": "2008_winter",
        "friendly_name": "Winter 2008",
        "filename": "/newsletters/Winter_2008.pdf",
    },
    {
        "id": "2008_summer",
        "friendly_name": "Summer 2008",
        "filename": "/newsletters/Spring_Summer_2008.pdf",
    },
    {
        "id": "2007_winter",
        "friendly_name": "Winter 2007",
        "filename": "/newsletters/Winter_2007.pdf",
    },
    {
        "id": "2007_summer",
        "friendly_name": "Summer 2007",
        "filename": "/newsletters/Summer_2007.pdf",
    },
    {
        "id": "2007_spring",
        "friendly_name": "Spring 2007",
        "filename": "/newsletters/Spring_2007.pdf",
    },
    {
        "id": "2006_winter",
        "friendly_name": "Winter 2006",
        "filename": "/newsletters/Winter_2006.pdf",
    },
    {
        "id": "2006_summer",
        "friendly_name": "Summer 2006",
        "filename": "/newsletters/Summer_2006.pdf",
    },
    {
        "id": "2006_spring",
        "friendly_name": "Spring 2006",
        "filename": "/newsletters/Spring_2006.pdf",
    },
    {
        "id": "2005_winter",
        "friendly_name": "Winter 2005",
        "filename": "/newsletters/Winter_2005.pdf",
    },
    {
        "id": "2005_summer",
        "friendly_name": "Summer 2005",
        "filename": "/newsletters/Summer_2005.pdf",
    },
    {
        "id": "2005_spring",
        "friendly_name": "Spring 2005",
        "filename": "/newsletters/Spring_2005.pdf",
    },
    {
        "id": "2004_winter",
        "friendly_name": "Winter 2004",
        "filename": "/newsletters/Winter_2004.pdf",
    },
    {
        "id": "2004_summer",
        "friendly_name": "Summer 2004",
        "filename": "/newsletters/Summer_2004.pdf",
    },
    {
        "id": "2004_spring",
        "friendly_name": "Spring 2004",
        "filename": "/newsletters/Spring_2004.pdf",
    },
    {
        "id": "2003_winter",
        "friendly_name": "Winter 2003",
        "filename": "/newsletters/Winter_2003.pdf",
    },
    {
        "id": "2003_summer",
        "friendly_name": "Summer 2003",
        "filename": "/newsletters/Summer_2003.pdf",
    },
    {
        "id": "2003_spring",
        "friendly_name": "Spring 2003",
        "filename": "/newsletters/Spring_2003.pdf",
    },
    {
        "id": "2002_winter",
        "friendly_name": "Winter 2002",
        "filename": "/newsletters/Winter_2002.pdf",
    },
    {
        "id": "2002_summer",
        "friendly_name": "Summer 2002",
        "filename": "/newsletters/Summer_2002.pdf",
    },
    {
        "id": "2002_spring",
        "friendly_name": "Spring 2002",
        "filename": "/newsletters/Spring_2002.pdf",
    },
    {
        "id": "2001_winter",
        "friendly_name": "Winter 2001",
        "filename": "/newsletters/Summer_Winter_2001.pdf",
    },
    {
        "id": "2001_spring",
        "friendly_name": "Spring 2001",
        "filename": "/newsletters/Spring_2001.pdf",
    },
    {
        "id": "2000_winter",
        "friendly_name": "Winter 2000",
        "filename": "/newsletters/winter_2000.pdf",
    },
    {
        "id": "2000_spring",
        "friendly_name": "Spring 2000",
        "filename": "/newsletters/Spring_2000.pdf",
    },
    {
        "id": "1999_winter",
        "friendly_name": "Winter 1999",
        "filename": "/newsletters/Winter_1999.pdf",
    },
    {
        "id": "1999_summer",
        "friendly_name": "Summer 1999",
        "filename": "/newsletters/Summer_1999.pdf",
    },
    {
        "id": "1998_winter",
        "friendly_name": "Winter 1998",
        "filename": "/newsletters/Winter_1998.pdf",
    },
    {
        "id": "1998_summer",
        "friendly_name": "Summer 1998",
        "filename": "/newsletters/Summer_1998.pdf",
    },
    {
        "id": "1998_spring",
        "friendly_name": "Spring 1998",
        "filename": "/newsletters/Spring_1998.pdf",
    },
    {
        "id": "1997_winter",
        "friendly_name": "Winter 1997",
        "filename": "/newsletters/winter_1997.pdf",
    },
    {
        "id": "1997_summer",
        "friendly_name": "Summer 1997",
        "filename": "/newsletters/Summer_1997.pdf",
    },
    {
        "id": "1997_spring",
        "friendly_name": "Spring 1997",
        "filename": "/newsletters/Spring_1997.pdf",
    },
    {
        "id": "1996_winter",
        "friendly_name": "Winter 1996",
        "filename": "/newsletters/Winter_1996.pdf",
    },
    {
        "id": "1996_summer",
        "friendly_name": "Summer 1996",
        "filename": "/newsletters/Summer_1996.pdf",
    },
    {
        "id": "1996_spring",
        "friendly_name": "Spring 1996",
        "filename": "/newsletters/Spring_1996.pdf",
    },
    {
        "id": "1995_winter",
        "friendly_name": "Winter 1995",
        "filename": "/newsletters/Winter_1995.pdf",
    },
    {
        "id": "1995_summer",
        "friendly_name": "Summer 1995",
        "filename": "/newsletters/summer_1995.pdf",
    },
    {
        "id": "1995_spring",
        "friendly_name": "Spring 1995",
        "filename": "/newsletters/Spring_1995.pdf",
    },
    {
        "id": "1994_winter",
        "friendly_name": "Winter 1994",
        "filename": "/newsletters/Winter_1994.pdf",
    },
    {
        "id": "1994_summer",
        "friendly_name": "Summer 1994",
        "filename": "/newsletters/summer_1994.pdf",
    },
    {
        "id": "1994_spring",
        "friendly_name": "Spring 1994",
        "filename": "/newsletters/Spring_1994.pdf",
    },
    {
        "id": "1993_winter",
        "friendly_name": "Winter 1993",
        "filename": "/newsletters/winter_1993.pdf",
    },
    {
        "id": "1993_summer",
        "friendly_name": "Summer 1993",
        "filename": "/newsletters/Summer_1993.pdf",
    },
    {
        "id": "1993_spring",
        "friendly_name": "Spring 1993",
        "filename": "/newsletters/Spring_1993.pdf",
    },
    {
        "id": "1992_winter",
        "friendly_name": "Winter 1992",
        "filename": "/newsletters/Winter_1992.pdf",
    },
    {
        "id": "1992_summer",
        "friendly_name": "Summer 1992",
        "filename": "/newsletters/Summer_1992.pdf",
    },
    {
        "id": "1992_spring",
        "friendly_name": "Spring 1992",
        "filename": "/newsletters/Spring_1992.pdf",
    },
    {
        "id": "1991_winter",
        "friendly_name": "Winter 1991",
        "filename": "/newsletters/Winter_1991.pdf",
    },
    {
        "id": "1991_summer",
        "friendly_name": "Summer 1991",
        "filename": "/newsletters/Summer_1991.pdf",
    },
    {
        "id": "1991_spring",
        "friendly_name": "Spring 1991",
        "filename": "/newsletters/Spring_1991.pdf",
    },
    {
        "id": "1990_winter",
        "friendly_name": "Winter 1990",
        "filename": "/newsletters/Winter_1990.pdf",
    },
    {
        "id": "1990_summer",
        "friendly_name": "Summer 1990",
        "filename": "/newsletters/Summer_1990.pdf",
    },
    {
        "id": "1990_spring",
        "friendly_name": "Spring 1990",
        "filename": "/newsletters/Spring_1990.pdf",
    },
    {
        "id": "1989_winter",
        "friendly_name": "Winter 1989",
        "filename": "/newsletters/Winter_1989.pdf",
    },
    {
        "id": "1989_summer",
        "friendly_name": "Summer 1989",
        "filename": "/newsletters/Summer_1989.pdf",
    },
    {
        "id": "1989_spring",
        "friendly_name": "Spring 1989",
        "filename": "/newsletters/Spring_1989.pdf",
    },
    {
        "id": "1988_summer",
        "friendly_name": "Summer 1988",
        "filename": "/newsletters/summer_1988.pdf",
    },
    {
        "id": "1988_spring",
        "friendly_name": "Spring 1988",
        "filename": "/newsletters/Spring_1988.pdf",
    },
    {
        "id": "1987_winter",
        "friendly_name": "Winter 1987",
        "filename": "/newsletters/Winter_1987.pdf",
    },
    {
        "id": "1987_summer",
        "friendly_name": "Summer 1987",
        "filename": "/newsletters/Summer_1987.pdf",
    },
    {
        "id": "1987_spring",
        "friendly_name": "Spring 1987",
        "filename": "/newsletters/Spring_1987.pdf",
    },
    {
        "id": "1986_winter",
        "friendly_name": "Winter 1986",
        "filename": "/newsletters/Winter_1986.pdf",
    },
    {
        "id": "1986_summer",
        "friendly_name": "Summer 1986",
        "filename": "/newsletters/Summer_1986.pdf",
    },
    {
        "id": "1986_spring",
        "friendly_name": "Spring 1986",
        "filename": "/newsletters/Spring_1986.pdf",
    },
]
