import os
import re

from django.conf import settings

# TODO:
# 1. tests!
# 4. how to deal with "previews" and "member" views?

ARTICLES = {
    "Spring 2021": '<p>Beeks, Graydon. "Alternate Performing Options for Handel\'s Op.2 Trio Sonatas found in Continental Sources," 1–3.</p><p>Kim, Minji. "2021 American Handel Society Conference: Scholarship, Performance, and Connection in the Age of COVID-19," 1, 4–5.</p>',
    "Summer 2021": '<p>Fehleisen, Fred. "Birmingham Baroque 2021 Conference Report," 1, 5.</p><p>Howard, Luke. "Boston, Birmingham, and the Reception of Robert Franz\'s Edition of Messiah," 1–4.</p>',
    "Winter 2021": '<p>Fehleisen, Fred. "Handel: Interactions and Influences"—London, November 19–21, 2021."</p><p>Maust, Paula. "Book Review: Alison C. DeSimone, The Power of Pastiche: Musical Miscellany and Cultural Identity in Early Eighteenth-Century England (Clemson, SC: Clemson University Press, 2021)."</p>',
    "Spring 2020": '<p>Beeks, Graydon. "John Langshaw as a Handel Copyist," 1–3.</p><p>DeSimone, Alison C. "My Summer on the J. Merrill Knapp Fellowship," 5.</p><p>Harris, Ellen T., "2020 London Handel Festival: Handel and the Hanoverians," 1, 4–5.</p>',
    "Summer 2020": '<p>Beeks, Graydon. "Handel and Improved Psalmody," 1–3.</p><p>Neff, Teresa M. "A Wealth of Music: Harry Christophers and the Handel and Haydn Society," 1, 4–5. ',
    "Winter 2020": 'Compton, Regina. "Hashtags and Handel:A Review of Acis and Galatea by the Haymarck Opera Company, 1–3.',
    "Spring 2019": '<p>Link, Nathan. "2019 American Handel Festival," 1–3.</p><p>Risinger, Mark. "Handel\'s Semele: The English Concert at Carnegie Hall," 1, 4–5.</p>',
    "Summer 2019": '<p>Beeks, Graydon, "Report from Halle," 1, 4–5.</p><p>Howard, Luke. "Ebenezer Prout (1835–1909) and Messiah: An Overdue Assessment," 1–3.</p>',
    "Winter 2019": '<p>Beeks, Graydon. "\'A Cosmic Notion\': Philharmonia Baroque Orchestra & Chorale," 1, 4–5.</p><p>McGeary, Thomas. "Book Review: Ursula Kirkendale, Georg Friedrich Händel, Francesco Maria Ruspoli e Roma," 1–3.</p>',
    "Spring 2018": 'Harris, Ellen T. "London Handel Festival 2018 and Cambridge Handel Opera Revived," 1–4.',
    "Summer 2018": '<p>Beeks, Graydon. "Report from Halle 2018," 1, 3–4.</p><p>Nott, Kenneth. "Handel\'s Blindness and its Effect on his Composing," 1–3.</p>',
    "Winter 2018": 'Ćurković, Ivan. "Handel and His Music for Patrons: 2018 Handel Institute Conference Report," 1–3.',
    "Spring 2017": '<p>Harris, Ellen T. "Springtime Handel Flowering," 3–4.</p><p>Lanfossi, Carlo. "American Handel Festival 2017: Conference Report," 1–2.</p><p>Risinger, Mark. "In Review: Ariodante and The Occasional Oratorio," 4–5.</p><p>Zazzo, Lawrence. "Giulio Cesare, Boston Baroque," 6.</p>',
    "Summer 2017": '<p>Beeks, Graydon. "Report from Halle," 1, 4–5.</p><p>Risinger, Mark. "Reflections on the Sources and Staging of Semele," 1–3.</p>',
    "Winter 2017": '<p>Beeks, Graydon. Joseph and his Brethren in San Francisco," 1, 5.</p><p>Hunter, David. "Peter Pasqualino, a Cellist in Handel Bands," 1–4.</p>',
    "Spring 2016": '<p>Farson, Helen. "Handel\'s Use of Fugue in Alexander\'s Feast," 1, 4–5.</p><p>Kim, Minji. "Handel\'s Saul at Boston\'s Symphony Hall," 5–6.</p><p>Shryock, Andrew. "The Early Career of Thomas Lowe, Oratorio Tenor," 1–3.</p>',
    "Summer 2016": '<p>Beeks, Graydon. "Report from Halle," 1, 4–5. </p><p>Beeks, Graydon. "Obituary for Andrew Porter (1928–2015)," 7.</p><p>DeSimone, Alison. "Handel\'s Greatest Hits: The Composer\'s Music in Eighteenth-Century Benefit Concerts," 1–3.</p><p>Rosand, Ellen. "Obituary for Alan Curtis (1934–2015)," 6.</p>',
    "Winter 2016": '<p>Beeks, Graydon. "Another Reference to Handel in the Montagu Correspondence," 1, 4.</p><p>Nissenbaum, Stephen. "The Long Strange Career of a Handel Misattribution, 1727–2013," 1–3.</p>',
    "Spring 2015": '<p>Beeks, Graydon. "Mirth, Melancholy, and the Future Mrs. Montagu," 1, 4–5.</p><p>Lee, Jonathan Rhodes. "Report of the 2015 Meeting of the American Handel Society, Iowa City, Iowa," 1–2.  </p><p>Ronish, Marty. "Theodora on the Left Coast," 3.</p><p>Ward, Marvin J. "Boston Baroque Production of Handel\'s Agrippina,\'" 6.</p>',
    "Summer 2015": '<p>Beeks, Graydon. "Report from Halle," 1–2. </p><p>Compton, Regina. "Of Heroes, Lovers, and Clowns: A Review of Alessandro at the Händel-Festspiele Halle," 6.</p><p>Farson, Helen. "Emmauelle Haïm in Los Angeles," 3.</p><p>Shoaff, Adam. "Handel in The Harmonicon," 1, 4–5.</p>',
    "Winter 2015": '<p>Gardner, Matthew. "Handel and His Eighteenth-Century Performers: The Handel Institute Conference, London," 1–3.</p><p>Harris, Ellen T. "Exhibition: Handel:  A Life with Friends Handel & Hendrix in London," 1, 4–5.</p>',
    "Spring 2014": '<p>Beeks, Graydon, "Theodora in Southern California," 5.</p><p>Roberts, John H. "Memories of Winton Dean (1916–2013)," 1–2.</p><p>"American Handel Society Conference, Princeton University, Abstracts (Part IV)," 3–4.</p>',
    "Summer 2014": '<p>Beeks, Graydon. "Report from Halle 2014," 4–6.</p><p>Strohm, Reinhard. "Handel: Opera and Ritual, Abstract of the Howard Serwer Lecture, Princeton, 22 February 2013," 3.</p>',
    "Winter 2014": '<p>Beeks, Graydon. "Christopher Hogwood Remembrance," 4–5.</p><p>Beeks, Graydon. "The Thomas Baker Collection Revisited," 6.</p>',
    "Spring 2013": '<p>"American Handel Society Conference, Princeton University, February 21–24, 2013, Abstracts (Part I)," 5–6.</p><p>Bazler, Corbett. "Conference Report: AHS Festival and Conference, February 21–24, 2013," 1–3.</p><p>Nott, Kenneth. "H&H Jephtha and Cambridge Jephtha Symposium," 4–5.</p>',
    "Summer 2013": '<p>"American Handel Society Conference, Princeton University, February 21–24, 2013, Abstracts (Part II)," 5–6.</p><p>Beeks, Graydon, "Report from Halle," 6.</p><p>Harris, Ellen T. "Handel\'s Almira and the Boston Early Music Festival 2013," 1–4.</p>',
    "Winter 2013": '<p>"American Handel Society Conference, Princeton University, February 21–24, 2013, Abstracts (Part III)," 4–6.</p><p>Beeks, Graydon. "What\'s in a name?" 1–3.</p>',
    "Summer 2012": '<p>Beeks, Graydon. "Report from Halle 2012," 4–6.</p><p>Ketterer, Robert. "Teseo: Chicago Opera Theater, April–May 2012," 1–3.</p>',
    "Winter 2012": '<p>"American Handel Society Festival 2013, Princeton University, Schedule," 1–5.</p>',
    "Spring 2011": '<p>"American Handel Society Conference, Seattle, Washington March 24–27, 2011, Abstracts (Part I)," 1–4.</p><p>Chrissochoidis, Ilias. "Handelian References in Richard Pococke\'s Early Correspondence (1734–7), 5–6.</p>',
    "Summer 2011": '<p>Beeks, Graydon. "Report from Halle 2011," 1, 3–4.</p><p>Beeks, Graydon. "Mrs. Montagu, the London Earthquakes and Handel," 5–6.</p>',
    "Winter 2011": '<p>"American Handel Society Conference, Seattle, Washington March 24–27, 2011, Abstracts (Part II)," 3–5.</p><p>"Remembering Paul Traver (1931–2011)," 1–2.</p>',
    "Spring 2010": '<p>Beeks, Graydon. "Two Handel Organ Projects," 1, 3.</p> <p>Nott, Kenneth. "\'Toiling at the Lower Employments of Life\' or Editing Handel," 4–6.</p>',
    "Summer 2010": '<p>Beeks, Graydon. "Report from Halle 2010," 1, 3–4.</p> <p>Roberts, John H. "Anthony Hicks Remembered," 1–2.</p>',
    "Winter 2010": '<p>Burrows, Donald. "Not Such a \'Low Employment\': Dr Johnson and Editing," 4–5.</p> <p>Ketterer, Robert C. "London as Athens: Teseo and Arianna in Creta," 1–3.</p>',
    "Spring 2009": '"American Handel Festival, Centre College, February 26–March 1, 2009, Abstracts," 1, 3–6.',
    "Summer 2009": '<p>Beeks, Graydon. "Report from Halle," 1, 4–5.</p><p>Beeks, Graydon. "Radamisto at Santa Fe Opera," 2</p> <p>Chrissochoidis, Ilias. "Music in Good Time and the Handelian Discord in 1745," 1–3.</p>',
    "Winter 2009": '<p>Beeks, Graydon. "Additional Sources for the Cannons Anthems," 1, 3–4.</p> <p>Beeks, Graydon. "Report from London," 4–5.</p> <p>"Handel in Seattle: the American Handel Festival 2011," 1–2.</p>',
    "Spring/Summer 2008": '<p>Beeks, Graydon. "Report from Halle 2008," 1, 3–4.</p> <p>Chrissochoidis, Ilias. "Oratorio À La Mode," 7–9.</p> <p>Ketterer, Robert. "Orlando: Chicago Opera Theater, June 2008," 1, 5–6.</p>',
    "Winter 2008": '<p>"American Handel Festival, Centre College, February 26–March 1, 2009, Schedule," 1–2.</p> <p>Nott, Kenneth. "Teaching Handel\'s Old Testament Oratorios," 1, 3–6.</p>',
    "Spring 2007": '"Handel at Princeton Conference Abstracts," 1–6.',
    "Summer 2007": '<p>Beeks, Graydon. "Report from Halle 2007," 1–3.</p><p>Burrows, Donald. "The \'Handel Documents\' Project," 1, 4.</p><p>Chrissochoidis, Ilias. "His Majesty\'s Choice: Esther in May 1732," 4–6.</p>',
    "Winter 2007": '<p>Beeks, Graydon. "The organ from the Chapel at Cannons," 5–6.</p><p>Heller, Wendy. "Reflections on Handel, Messiah, and Anti-Judaism: A Year Later," 1, 4.</p><p>"Dr. Siegfried Flesch," 1.</p>',
    "Spring 2006": '<p>Beeks, Graydon. "A New Referencce to the Fireworks Music," 6.</p><p>Chrissochoidis, Ilias. "Charles Handell, Esq. (?–1776)," 1, 3.</p>',
    "Summer 2006": '<p>Beeks, Graydon. "Report from Halle 2006," 1, 5–6.</p><p>Towe, Teri Noel. "Tribute to a Noted Authority on Handel & Early Music," 1, 3.</p>',
    "Winter 2006": '<p>Beeks, Graydon. "Some Overlooked Reference to Handel," 1, 3–4.</p><p>Richter, Klaus P. "Handle Premiere in Munich," 6.</p>',
    "Spring 2005": '<p>"American Handel Society Conference, Santa Fe, Abstracts I," 2, 4.</p><p>Beeks, Graydon. "Stanley Sadie (1930–2005)," 1, 3.</p><p>Ketterer, Robert. "La Resurrezione at Chicago Opera Theater," 5.</p><p>Link, Nathan, and Zach Victor. "Report on Handel in Santa Fe," 1, 3.</p>',
    "Summer 2005": '<p>"American Handel Society Conference, Santa Fe, Abstracts II," 2, 5.</p> <p>Beeks, Graydon. "Howard Serwer Memorial Lecture: \'Private Patronage of Church Music in the Reign of George I\' Abstract," 1, 3.</p> <p>Beeks, Graydon. "Report from Halle 2005," 1, 3–4.</p>',
    "Winter 2005": '<p>Burrows, Donald. "The Trail of the Samson Word-Books," 1, 4–5.</p> <p>Harris, Ellen T. "Two Festival Reports," 1–3.</p>',
    "Spring 2004": '<p>Beeks, Graydon. "The Thomas Baker Collection," 1, 3</p><p>Gudger, William D. "Tamerlano at Spoleto Festival USA 2003," 1, 4–5.</p>',
    "Summer 2004": 'Beeks, Graydon. "Report from Halle," 1, 3–4.',
    "Winter 2004": '<p>Burrows, Donald. "Thomas Baker\'s Word-Book for Samson," 6.</p><p>Hogg, Katherine. "The Gerald Coke Handel Collection," 1, 3, 5.</p>',
    "Spring 2003": '<p>Best, Terence. "\'Handel Editions Past and Present\' AHS Howard Serwer Lecture 2003, Abstract," 5.</p><p>Nott, Kenneth. "A Pilgrimage to Iowa," 1, 3. </p><p>Saslow, James M. "\'For I would sing of Boys Loved by the Gods\': The Orphic Impulse in Cultural History, Abstract," 4.</p><p>"The Triumphs of Thusnelda: An Imperialist Myth in Early Opera," 1, 3.</p>',
    "Summer 2003": '<p>Beeks, Graydon. "Handel Festival in Halle 2003," 1, 3–4.</p><p>Ketterer, Robert. "A Tacitist Agrippina: Chicago Opera Theater, April–May 2003," 1, 4–6.</p>',
    "Winter 2003": '<p>Nott, Kenneth. "Houston grand Opera\'s Guilio Cesare," 1, 3.</p><p>Ronish, Marty. "In Memoriam: Keiichiro Watanabe," 1, 5.</p>',
    "Spring 2002": '<p>Burrows, Donald. "A Tribute to Twenty Years of The Marland Handel Festival," 1, 5.</p><p>King, Richard. "Overview of an Historic Festival," 1, 3</p>',
    "Summer 2002": '<p>Ketterer, Robert. "Handel in Iowa, February 27–March 2, 2003," 1, 3. </p><p>Ketterer, Robert. "Semele, Chicago opera Theater, May 2002," 1, 3–5.</p>',
    "Winter 2002": '<p>"Handel in Iowa, Schedule," 1, 3–4.</p><p>"Philip Brett," 1, 3.</p>',
    "Spring 2001": '<p>Gudger, William. "Rinaldo at City Opera," 1, 10.</p><p>Ketterer, Robert. "Handel\'s Scipione and the Neutralization of Politics," 1, 4–8.</p>',
    "Winter 2001": '<p>Hunter, David. "Archival Challenges and Solutions," 1, 4–5.</p><p>Vickers, David. "London Sings Hallelujah: A Report from the Long-Awaited Handel House Museum," 1, 6–7.</p>',
    "Spring 2000": '<p>Landgraf, Annette. "The \'Sea of Choruses\': Concerning the New HHA Edition of Israel in Egypt," trans. Jarl Hulbert and A. Landraf, 13–14.</p><p>King, Richard, and Paul Traver, "Howard Serwer (1928–2000), 1, 8.</p><p>"Reminiscences of Howard Serwer," 8–10.</p><p>"Three Ladies of Handel\'s Will," 1, 4.</p>',
    "Winter 2000": '<p>Burrows, Donald. "Handel in London," 1, 3</p><p>"Maryland Handel Festival 2001, Schedule," 1, 6</p>',
    "Summer 1999": 'King, Richard G. "On Princess Anne\'s Patronage of the Second Academy," 1, 6.',
    "Winter 1999": '<p>"Maryland Handel Festival 2000, Schedule," 1, 6.</p><p>Traver, Paul. "Handel: Great Among the Nations," 1, 3.</p>',
    "Spring 1998": '"The Hero in Drag: Omphale, Dejanira, and the Emasculization of Hercules," 1, 6.',
    "Summer 1998": 'Beeks, Graydon. "A Curious Handel Performance at Keynsham," 1, 6.',
    "Winter 1998": '<p>Hunter, David. "Handel, John Hughes and Mary, Countess Cowper," 1, 6.</p><p>"1998 Maryland Handel Festival and American Handel Society Conference Abstracts," 3s–6.</p>',
    "Spring 1997": 'Beeks, Graydon. "More Handel Anthems in American Libraries," 1, 6.',
    "Summer 1997": '<p>Facio, Iter. "The Handel Festivals in Göttingen (29 May to 2 June) and Halle 5 to 10 June)," 1, 3–4, 7.<p><p>Leissa, Brad. "High-Tech Handel," 1, 5.<p>',
    "Winter 1997": '<p>Hunter, David. "Advice to Mr. Handel," 3, 6.<p><p>Sadie, Julie Anne. "The Handel House Museum and the Byrne Collection," 1, 4–5.<p>',
    "Spring 1996": '<p>Harris, Ellen T. "Xerxes at Boston Lyric Opera, March 6–17, 1996," 1–2, 4.<p><p>Hunter, David. "The Oxford Musical Society\'s Manuscript of Handel\'s Coronation Anthems at Texas," 1, 3, 5.<p><p>Rosand, Ellen. "William Christie\'s Orlando at the Brooklyn Academy of Music February 9–13, 1996," 3.<p>',
    "Summer 1996": '<p>Beeks, Graydon. "Handel and Lady Cobham," 1–2, 4.<p><p>Harris, Ellen T. "Handel on Stage," 1, 3–6.<p>',
    "Winter 1996": '<p>"Abstracts of the 1996 American Handel Society Conference," 1, 3, 6.<p><p>Burrows, Donald. "Mr Handel\'s Friends: Contemporary Accounts of the Composer from the Papers of James Harris," 1, 4–6.<p>',
    "Spring 1995": '<p>Dean, Winton. "1994 American Handel Society Lecture: Handel\'s Operas in the Theater," 1–2.</p><p>Corn, Michael. "The Intellectual Context of Handel\'s Solomon," 1, 3–5.</p>',
    "Summer 1995": '<p>Auner, Joseph Henry. "Schoenberg and Handel in 1933," 1, 5–6.</p><p>Cervantes, Xavier. "Ezio in Paris," 7.</p><p>Facio, Iter. "The Forty-fourth Händel-Festspiele, Halle/Saale June 1995," 3, 9.</p><p>Harris, Ellen T. "Review of Farnelli," 1, 4.</p><p>Winemiller, John T. "Marcell\'s Bear and a St. Paul Alcina," 2, 8.</p>',
    "Winter 1995": '<p>Beeks, Graydon. "Anna Strada del Pò: Handel\'s \'New\' Soprano," 3.</p><p>Beeks, Graydon. "Handel Queen Anne," 1, 6.</p><p>Fregosi, Bill. "Tamerlano at Glimmerglass," 1–2.</p><p>Lindgren, Lowell. "Joshua in Boston," 5</p>',
    "Spring 1994": '<p>Bennett, Shelley M. "Roubiliac\'s Handel," 1, 4.</p><p>Cervantes, Xavier. "Report from Montpellier," 5.</p><p>Facio, Iter. "Report form Karlsruhe," 1, 4. </p>',
    "Summer 1994": '<p>Facio, Iter. "Report from Halle," 1, 3.</p><p>Gossmann, Otto. "Report from Göttingen," 1, 4.</p>',
    "Winter 1994": '<p>Perez, Karen, and Graydon Beeks. "Madame Melba Sings Handel," 1–2, 7.</p><p>"1994 American Handel Society Conference Abstracts," 3–6.</p>',
    "Spring 1993": '<p>Mann, Alfred. "In Memoriam: Walther Siegmund-Schultze," 2.</p><p>Roberts, John H. "1992 American Handel Society Lecture: \'The Song for St. Cecilia\'s Day and Handel\'s Borrowing from Other Composers,\'" 1, 5.</p><p>Serwer, Howard, and Paul Traver. "J. Merrill Knapp 1914–1993," 1–2, 5.</p>',
    "Summer 1993": '<p>Beeks, Graydon. "Handelian Keyboards," 1, 9.</p><p>Corneilson, Paul. "Mozart, Vogler, and Messiah," 2–3.</p><p>Facio, Iter. "Report from Germany," 1, 6–8.</p><p>Winemiller, John T. "Borrowing, Copyright, and Proprietary Authorship," 4–5.</p>',
    "Winter 1993": '<p>Baselt, Bernd. "Handel\'s Oboe Concerto HWV 287: Contemporary Manuscript Source Rediscovered," 4.</p><p>Cervantes, Xavier. "Report from Montpellier," 4.</p><p>Facio, Iter. "Report from London," 1, 3.</p><p>Fleischhauer, Günter. "Professor Dr. phil, habil. Bernd Baselt (1934–1993): In memoriam," 1–2.</p>',
    "Spring 1992": '<p>Beeks, Graydon. "Messiah Anniversary: Some Further Thoughts," 1, 4.</p><p>Brainard, Paul. "Abstract of the 1991 American Handel Society Lecture: \'Bach and Handel: Another Look,\'" 2, 8.</p><p>Rogers, Patrick J. "Book Review of David Ledbetter, Continuo Playing According to Handel: His Figured Bass Exercises (Oxford, 1990)," 2, 5–6.</p><p>Serwer, Howard. "Agrippina," 1, 4–5.</p>',
    "Summer 1992": '<p>Beeks, Graydon. "Göttingen 1992," 2.</p><p>Facio, Iter. "Halle 1992," 1, 5.</p><p>King, Richard G. "On Princess Anne\'s Lessons with Handel," 1, 4.</p>',
    "Winter 1992": '<p>"Abstracts of the 1992 American Handel Society Conference," 3–6.</p><p>Beeks, Graydon. "Chichester Exhibition," 1, 7</p><p>McGegan, Nicholas. Book Review of Patrick J. Rogers, Contiuo Realization in Handel\'s Vocal Music (Ann Arbor, 1988), 2.</p>',
    "Spring 1991": 'Olbrych, Judith Connor. "Handel in Dwight\'s Journal of Music," 1, 6–7.',
}


class NewslettersData:
    def __init__(self):
        self.newsletter_filenames = os.listdir(
            "americanhandelsociety_app/static/newsletters"
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
            data["filename"] = f"newsletters/{filename}"
            data["articles"] = ARTICLES.get(data["friendly_name"], "")

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
        "filename": "newsletters/Handel_Summer_2020.pdf",
        "articles": '<p>Beeks, Graydon. "Handel and Improved Psalmody," 1–3.</p><p>Neff, Teresa M. "A Wealth of Music: Harry Christophers and the Handel and Haydn Society," 1, 4–5. ',
    },
    {
        "id": "2020_spring",
        "friendly_name": "Spring 2020",
        "filename": "newsletters/Handel_Spring_2020.pdf",
        "articles": '<p>Beeks, Graydon. "John Langshaw as a Handel Copyist," 1–3.</p><p>DeSimone, Alison C. "My Summer on the J. Merrill Knapp Fellowship," 5.</p><p>Harris, Ellen T., "2020 London Handel Festival: Handel and the Hanoverians," 1, 4–5.</p>',
    },
    {
        "id": "2019_winter",
        "friendly_name": "Winter 2019",
        "filename": "newsletters/Handel_Winter_2019.pdf",
        "articles": '<p>Beeks, Graydon. "\'A Cosmic Notion\': Philharmonia Baroque Orchestra & Chorale," 1, 4–5.</p><p>McGeary, Thomas. "Book Review: Ursula Kirkendale, Georg Friedrich Händel, Francesco Maria Ruspoli e Roma," 1–3.</p>',
    },
    {
        "id": "2019_summer",
        "friendly_name": "Summer 2019",
        "filename": "newsletters/Handel_Summer_2019.pdf",
        "articles": '<p>Beeks, Graydon, "Report from Halle," 1, 4–5.</p><p>Howard, Luke. "Ebenezer Prout (1835–1909) and Messiah: An Overdue Assessment," 1–3.</p>',
    },
    {
        "id": "2019_spring",
        "friendly_name": "Spring 2019",
        "filename": "newsletters/Handel_Spring_2019.pdf",
        "articles": '<p>Link, Nathan. "2019 American Handel Festival," 1–3.</p><p>Risinger, Mark. "Handel\'s Semele: The English Concert at Carnegie Hall," 1, 4–5.</p>',
    },
    {
        "id": "2018_winter",
        "friendly_name": "Winter 2018",
        "filename": "newsletters/Handel_Winter_2018.pdf",
        "articles": 'Ćurković, Ivan. "Handel and His Music for Patrons: 2018 Handel Institute Conference Report," 1–3.',
    },
    {
        "id": "2018_summer",
        "friendly_name": "Summer 2018",
        "filename": "newsletters/Handel_Summer_2018_Web.pdf",
        "articles": '<p>Beeks, Graydon. "Report from Halle 2018," 1, 3–4.</p><p>Nott, Kenneth. "Handel\'s Blindness and its Effect on his Composing," 1–3.</p>',
    },
    {
        "id": "2018_spring",
        "friendly_name": "Spring 2018",
        "filename": "newsletters/Handel_Spring_2018.pdf",
        "articles": 'Harris, Ellen T. "London Handel Festival 2018 and Cambridge Handel Opera Revived," 1–4.',
    },
    {
        "id": "2017_winter",
        "friendly_name": "Winter 2017",
        "filename": "newsletters/Handel_Winter_2017.pdf",
        "articles": '<p>Beeks, Graydon. Joseph and his Brethren in San Francisco," 1, 5.</p><p>Hunter, David. "Peter Pasqualino, a Cellist in Handel Bands," 1–4.</p>',
    },
    {
        "id": "2017_summer",
        "friendly_name": "Summer 2017",
        "filename": "newsletters/Handel_Summer_2017.pdf",
        "articles": '<p>Beeks, Graydon. "Report from Halle," 1, 4–5.</p><p>Risinger, Mark. "Reflections on the Sources and Staging of Semele," 1–3.</p>',
    },
    {
        "id": "2017_spring",
        "friendly_name": "Spring 2017",
        "filename": "newsletters/AHS Newsletter_Spring_2017_.pdf",
        "articles": '<p>Harris, Ellen T. "Springtime Handel Flowering," 3–4.</p><p>Lanfossi, Carlo. "American Handel Festival 2017: Conference Report," 1–2.</p><p>Risinger, Mark. "In Review: Ariodante and The Occasional Oratorio," 4–5.</p><p>Zazzo, Lawrence. "Giulio Cesare, Boston Baroque," 6.</p>',
    },
    {
        "id": "2016_winter",
        "friendly_name": "Winter 2016",
        "filename": "newsletters/Handel_Winter_2016_WEB.pdf",
        "articles": '<p>Beeks, Graydon. "Another Reference to Handel in the Montagu Correspondence," 1, 4.</p><p>Nissenbaum, Stephen. "The Long Strange Career of a Handel Misattribution, 1727–2013," 1–3.</p>',
    },
    {
        "id": "2016_summer",
        "friendly_name": "Summer 2016",
        "filename": "newsletters/Handel_Summer_2016_WEB.pdf",
        "articles": '<p>Beeks, Graydon. "Report from Halle," 1, 4–5. </p><p>Beeks, Graydon. "Obituary for Andrew Porter (1928–2015)," 7.</p><p>DeSimone, Alison. "Handel\'s Greatest Hits: The Composer\'s Music in Eighteenth-Century Benefit Concerts," 1–3.</p><p>Rosand, Ellen. "Obituary for Alan Curtis (1934–2015)," 6.</p>',
    },
    {
        "id": "2016_spring",
        "friendly_name": "Spring 2016",
        "filename": "newsletters/Handel_Spring_2016_WEB.pdf",
        "articles": '<p>Farson, Helen. "Handel\'s Use of Fugue in Alexander\'s Feast," 1, 4–5.</p><p>Kim, Minji. "Handel\'s Saul at Boston\'s Symphony Hall," 5–6.</p><p>Shryock, Andrew. "The Early Career of Thomas Lowe, Oratorio Tenor," 1–3.</p>',
    },
    {
        "id": "2015_winter",
        "friendly_name": "Winter 2015",
        "filename": "newsletters/Handel_Winter_2015_WEB.pdf",
        "articles": '<p>Gardner, Matthew. "Handel and His Eighteenth-Century Performers: The Handel Institute Conference, London," 1–3.</p><p>Harris, Ellen T. "Exhibition: Handel:  A Life with Friends Handel & Hendrix in London," 1, 4–5.</p>',
    },
    {
        "id": "2015_summer",
        "friendly_name": "Summer 2015",
        "filename": "newsletters/Handel_Summer_2015_WEB (1).pdf",
        "articles": '<p>Beeks, Graydon. "Report from Halle," 1–2. </p><p>Compton, Regina. "Of Heroes, Lovers, and Clowns: A Review of Alessandro at the Händel-Festspiele Halle," 6.</p><p>Farson, Helen. "Emmauelle Haïm in Los Angeles," 3.</p><p>Shoaff, Adam. "Handel in The Harmonicon," 1, 4–5.</p>',
    },
    {
        "id": "2015_spring",
        "friendly_name": "Spring 2015",
        "filename": "newsletters/Handel_Spring_2015_WEB.pdf",
        "articles": '<p>Beeks, Graydon. "Mirth, Melancholy, and the Future Mrs. Montagu," 1, 4–5.</p><p>Lee, Jonathan Rhodes. "Report of the 2015 Meeting of the American Handel Society, Iowa City, Iowa," 1–2.  </p><p>Ronish, Marty. "Theodora on the Left Coast," 3.</p><p>Ward, Marvin J. "Boston Baroque Production of Handel\'s Agrippina,\'" 6.</p>',
    },
    {
        "id": "2014_winter",
        "friendly_name": "Winter 2014",
        "filename": "newsletters/Handel_Winter_2014_Web.pdf",
        "articles": '<p>Beeks, Graydon. "Christopher Hogwood Remembrance," 4–5.</p><p>Beeks, Graydon. "The Thomas Baker Collection Revisited," 6.</p>',
    },
    {
        "id": "2014_summer",
        "friendly_name": "Summer 2014",
        "filename": "newsletters/Handel_Summer_2014_Web.pdf",
        "articles": '<p>Beeks, Graydon. "Report from Halle 2014," 4–6.</p><p>Strohm, Reinhard. "Handel: Opera and Ritual, Abstract of the Howard Serwer Lecture, Princeton, 22 February 2013," 3.</p>',
    },
    {
        "id": "2014_spring",
        "friendly_name": "Spring 2014",
        "filename": "newsletters/Handel_Spring_2014_Web.pdf",
        "articles": '<p>Beeks, Graydon, "Theodora in Southern California," 5.</p><p>Roberts, John H. "Memories of Winton Dean (1916–2013)," 1–2.</p><p>"American Handel Society Conference, Princeton University, Abstracts (Part IV)," 3–4.</p>',
    },
    {
        "id": "2013_winter",
        "friendly_name": "Winter 2013",
        "filename": "newsletters/AHS_Newsletter_Winter_2013.pdf",
        "articles": '<p>"American Handel Society Conference, Princeton University, February 21–24, 2013, Abstracts (Part III)," 4–6.</p><p>Beeks, Graydon. "What\'s in a name?" 1–3.</p>',
    },
    {
        "id": "2013_summer",
        "friendly_name": "Summer 2013",
        "filename": "newsletters/AHS_Newsletter_Summer_2013.pdf",
        "articles": '<p>"American Handel Society Conference, Princeton University, February 21–24, 2013, Abstracts (Part II)," 5–6.</p><p>Beeks, Graydon, "Report from Halle," 6.</p><p>Harris, Ellen T. "Handel\'s Almira and the Boston Early Music Festival 2013," 1–4.</p>',
    },
    {
        "id": "2013_spring",
        "friendly_name": "Spring 2013",
        "filename": "newsletters/AHS_Newsletter_Spring_2013.pdf",
        "articles": '<p>"American Handel Society Conference, Princeton University, February 21–24, 2013, Abstracts (Part I)," 5–6.</p><p>Bazler, Corbett. "Conference Report: AHS Festival and Conference, February 21–24, 2013," 1–3.</p><p>Nott, Kenneth. "H&H Jephtha and Cambridge Jephtha Symposium," 4–5.</p>',
    },
    {
        "id": "2012_winter",
        "friendly_name": "Winter 2012",
        "filename": "newsletters/HandelNewsletter_Winter_2012.pdf",
        "articles": '<p>"American Handel Society Festival 2013, Princeton University, Schedule," 1–5.</p>',
    },
    {
        "id": "2012_summer",
        "friendly_name": "Summer 2012",
        "filename": "newsletters/Handel_Summer_2012_Proof.pdf",
        "articles": '<p>Beeks, Graydon. "Report from Halle 2012," 4–6.</p><p>Ketterer, Robert. "Teseo: Chicago Opera Theater, April–May 2012," 1–3.</p>',
    },
    {
        "id": "2011_winter",
        "friendly_name": "Winter 2011",
        "filename": "newsletters/AHSNewsletter_Winter_2011.pdf",
        "articles": '<p>"American Handel Society Conference, Seattle, Washington March 24–27, 2011, Abstracts (Part II)," 3–5.</p><p>"Remembering Paul Traver (1931–2011)," 1–2.</p>',
    },
    {
        "id": "2011_summer",
        "friendly_name": "Summer 2011",
        "filename": "newsletters/AHSNewsletter_Summer_2011.pdf",
        "articles": '<p>Beeks, Graydon. "Report from Halle 2011," 1, 3–4.</p><p>Beeks, Graydon. "Mrs. Montagu, the London Earthquakes and Handel," 5–6.</p>',
    },
    {
        "id": "2011_spring",
        "friendly_name": "Spring 2011",
        "filename": "newsletters/AHSNewsletter_Spring_2011.pdf",
        "articles": '<p>"American Handel Society Conference, Seattle, Washington March 24–27, 2011, Abstracts (Part I)," 1–4.</p><p>Chrissochoidis, Ilias. "Handelian References in Richard Pococke\'s Early Correspondence (1734–7), 5–6.</p>',
    },
    {
        "id": "2010_winter",
        "friendly_name": "Winter 2010",
        "filename": "newsletters/Winter_2010.pdf",
        "articles": '<p>Burrows, Donald. "Not Such a \'Low Employment\': Dr Johnson and Editing," 4–5.</p> <p>Ketterer, Robert C. "London as Athens: Teseo and Arianna in Creta," 1–3.</p>',
    },
    {
        "id": "2010_summer",
        "friendly_name": "Summer 2010",
        "filename": "newsletters/Summer_2010.pdf",
        "articles": '<p>Beeks, Graydon. "Report from Halle 2010," 1, 3–4.</p> <p>Roberts, John H. "Anthony Hicks Remembered," 1–2.</p>',
    },
    {
        "id": "2010_spring",
        "friendly_name": "Spring 2010",
        "filename": "newsletters/Handel_Spring_2010_PROOF.pdf",
        "articles": '<p>Beeks, Graydon. "Two Handel Organ Projects," 1, 3.</p> <p>Nott, Kenneth. "\'Toiling at the Lower Employments of Life\' or Editing Handel," 4–6.</p>',
    },
    {
        "id": "2009_winter",
        "friendly_name": "Winter 2009",
        "filename": "newsletters/Winter_2009.pdf",
        "articles": '<p>Beeks, Graydon. "Additional Sources for the Cannons Anthems," 1, 3–4.</p> <p>Beeks, Graydon. "Report from London," 4–5.</p> <p>"Handel in Seattle: the American Handel Festival 2011," 1–2.</p>',
    },
    {
        "id": "2009_summer",
        "friendly_name": "Summer 2009",
        "filename": "newsletters/Summer_2009.pdf",
        "articles": '<p>Beeks, Graydon. "Report from Halle," 1, 4–5.</p><p>Beeks, Graydon. "Radamisto at Santa Fe Opera," 2</p> <p>Chrissochoidis, Ilias. "Music in Good Time and the Handelian Discord in 1745," 1–3.</p>',
    },
    {
        "id": "2009_spring",
        "friendly_name": "Spring 2009",
        "filename": "newsletters/Spring_2009No.1.pdf",
        "articles": '"American Handel Festival, Centre College, February 26–March 1, 2009, Abstracts," 1, 3–6.',
    },
    {
        "id": "2008_winter",
        "friendly_name": "Winter 2008",
        "filename": "newsletters/Winter_2008.pdf",
        "articles": '<p>"American Handel Festival, Centre College, February 26–March 1, 2009, Schedule," 1–2.</p> <p>Nott, Kenneth. "Teaching Handel\'s Old Testament Oratorios," 1, 3–6.</p>',
    },
    {
        "id": "2008_summer",
        "friendly_name": "Summer 2008",
        "filename": "newsletters/Spring_Summer_2008.pdf",
        "articles": "",
    },
    {
        "id": "2007_winter",
        "friendly_name": "Winter 2007",
        "filename": "newsletters/Winter_2007.pdf",
        "articles": '<p>Beeks, Graydon. "The organ from the Chapel at Cannons," 5–6.</p><p>Heller, Wendy. "Reflections on Handel, Messiah, and Anti-Judaism: A Year Later," 1, 4.</p><p>"Dr. Siegfried Flesch," 1.</p>',
    },
    {
        "id": "2007_summer",
        "friendly_name": "Summer 2007",
        "filename": "newsletters/Summer_2007.pdf",
        "articles": '<p>Beeks, Graydon. "Report from Halle 2007," 1–3.</p><p>Burrows, Donald. "The \'Handel Documents\' Project," 1, 4.</p><p>Chrissochoidis, Ilias. "His Majesty\'s Choice: Esther in May 1732," 4–6.</p>',
    },
    {
        "id": "2007_spring",
        "friendly_name": "Spring 2007",
        "filename": "newsletters/Spring_2007.pdf",
        "articles": '"Handel at Princeton Conference Abstracts," 1–6.',
    },
    {
        "id": "2006_winter",
        "friendly_name": "Winter 2006",
        "filename": "newsletters/Winter_2006.pdf",
        "articles": '<p>Beeks, Graydon. "Some Overlooked Reference to Handel," 1, 3–4.</p><p>Richter, Klaus P. "Handle Premiere in Munich," 6.</p>',
    },
    {
        "id": "2006_summer",
        "friendly_name": "Summer 2006",
        "filename": "newsletters/Summer_2006.pdf",
        "articles": '<p>Beeks, Graydon. "Report from Halle 2006," 1, 5–6.</p><p>Towe, Teri Noel. "Tribute to a Noted Authority on Handel & Early Music," 1, 3.</p>',
    },
    {
        "id": "2006_spring",
        "friendly_name": "Spring 2006",
        "filename": "newsletters/Spring_2006.pdf",
        "articles": '<p>Beeks, Graydon. "A New Referencce to the Fireworks Music," 6.</p><p>Chrissochoidis, Ilias. "Charles Handell, Esq. (?–1776)," 1, 3.</p>',
    },
    {
        "id": "2005_winter",
        "friendly_name": "Winter 2005",
        "filename": "newsletters/Winter_2005.pdf",
        "articles": '<p>Burrows, Donald. "The Trail of the Samson Word-Books," 1, 4–5.</p> <p>Harris, Ellen T. "Two Festival Reports," 1–3.</p>',
    },
    {
        "id": "2005_summer",
        "friendly_name": "Summer 2005",
        "filename": "newsletters/Summer_2005.pdf",
        "articles": '<p>"American Handel Society Conference, Santa Fe, Abstracts II," 2, 5.</p> <p>Beeks, Graydon. "Howard Serwer Memorial Lecture: \'Private Patronage of Church Music in the Reign of George I\' Abstract," 1, 3.</p> <p>Beeks, Graydon. "Report from Halle 2005," 1, 3–4.</p>',
    },
    {
        "id": "2005_spring",
        "friendly_name": "Spring 2005",
        "filename": "newsletters/Spring_2005.pdf",
        "articles": '<p>"American Handel Society Conference, Santa Fe, Abstracts I," 2, 4.</p><p>Beeks, Graydon. "Stanley Sadie (1930–2005)," 1, 3.</p><p>Ketterer, Robert. "La Resurrezione at Chicago Opera Theater," 5.</p><p>Link, Nathan, and Zach Victor. "Report on Handel in Santa Fe," 1, 3.</p>',
    },
    {
        "id": "2004_winter",
        "friendly_name": "Winter 2004",
        "filename": "newsletters/Winter_2004.pdf",
        "articles": '<p>Burrows, Donald. "Thomas Baker\'s Word-Book for Samson," 6.</p><p>Hogg, Katherine. "The Gerald Coke Handel Collection," 1, 3, 5.</p>',
    },
    {
        "id": "2004_summer",
        "friendly_name": "Summer 2004",
        "filename": "newsletters/Summer_2004.pdf",
        "articles": 'Beeks, Graydon. "Report from Halle," 1, 3–4.',
    },
    {
        "id": "2004_spring",
        "friendly_name": "Spring 2004",
        "filename": "newsletters/Spring_2004.pdf",
        "articles": '<p>Beeks, Graydon. "The Thomas Baker Collection," 1, 3</p><p>Gudger, William D. "Tamerlano at Spoleto Festival USA 2003," 1, 4–5.</p>',
    },
    {
        "id": "2003_winter",
        "friendly_name": "Winter 2003",
        "filename": "newsletters/Winter_2003.pdf",
        "articles": '<p>Nott, Kenneth. "Houston grand Opera\'s Guilio Cesare," 1, 3.</p><p>Ronish, Marty. "In Memoriam: Keiichiro Watanabe," 1, 5.</p>',
    },
    {
        "id": "2003_summer",
        "friendly_name": "Summer 2003",
        "filename": "newsletters/Summer_2003.pdf",
        "articles": '<p>Beeks, Graydon. "Handel Festival in Halle 2003," 1, 3–4.</p><p>Ketterer, Robert. "A Tacitist Agrippina: Chicago Opera Theater, April–May 2003," 1, 4–6.</p>',
    },
    {
        "id": "2003_spring",
        "friendly_name": "Spring 2003",
        "filename": "newsletters/Spring_2003.pdf",
        "articles": '<p>Best, Terence. "\'Handel Editions Past and Present\' AHS Howard Serwer Lecture 2003, Abstract," 5.</p><p>Nott, Kenneth. "A Pilgrimage to Iowa," 1, 3. </p><p>Saslow, James M. "\'For I would sing of Boys Loved by the Gods\': The Orphic Impulse in Cultural History, Abstract," 4.</p><p>"The Triumphs of Thusnelda: An Imperialist Myth in Early Opera," 1, 3.</p>',
    },
    {
        "id": "2002_winter",
        "friendly_name": "Winter 2002",
        "filename": "newsletters/Winter_2002.pdf",
        "articles": '<p>"Handel in Iowa, Schedule," 1, 3–4.</p><p>"Philip Brett," 1, 3.</p>',
    },
    {
        "id": "2002_summer",
        "friendly_name": "Summer 2002",
        "filename": "newsletters/Summer_2002.pdf",
        "articles": '<p>Ketterer, Robert. "Handel in Iowa, February 27–March 2, 2003," 1, 3. </p><p>Ketterer, Robert. "Semele, Chicago opera Theater, May 2002," 1, 3–5.</p>',
    },
    {
        "id": "2002_spring",
        "friendly_name": "Spring 2002",
        "filename": "newsletters/Spring_2002.pdf",
        "articles": '<p>Burrows, Donald. "A Tribute to Twenty Years of The Marland Handel Festival," 1, 5.</p><p>King, Richard. "Overview of an Historic Festival," 1, 3</p>',
    },
    {
        "id": "2001_winter",
        "friendly_name": "Winter 2001",
        "filename": "newsletters/Summer_Winter_2001.pdf",
        "articles": '<p>Hunter, David. "Archival Challenges and Solutions," 1, 4–5.</p><p>Vickers, David. "London Sings Hallelujah: A Report from the Long-Awaited Handel House Museum," 1, 6–7.</p>',
    },
    {
        "id": "2001_spring",
        "friendly_name": "Spring 2001",
        "filename": "newsletters/Spring_2001.pdf",
        "articles": '<p>Gudger, William. "Rinaldo at City Opera," 1, 10.</p><p>Ketterer, Robert. "Handel\'s Scipione and the Neutralization of Politics," 1, 4–8.</p>',
    },
    {
        "id": "2000_winter",
        "friendly_name": "Winter 2000",
        "filename": "newsletters/winter_2000.pdf",
        "articles": '<p>Burrows, Donald. "Handel in London," 1, 3</p><p>"Maryland Handel Festival 2001, Schedule," 1, 6</p>',
    },
    {
        "id": "2000_spring",
        "friendly_name": "Spring 2000",
        "filename": "newsletters/Spring_2000.pdf",
        "articles": '<p>Landgraf, Annette. "The \'Sea of Choruses\': Concerning the New HHA Edition of Israel in Egypt," trans. Jarl Hulbert and A. Landraf, 13–14.</p><p>King, Richard, and Paul Traver, "Howard Serwer (1928–2000), 1, 8.</p><p>"Reminiscences of Howard Serwer," 8–10.</p><p>"Three Ladies of Handel\'s Will," 1, 4.</p>',
    },
    {
        "id": "1999_winter",
        "friendly_name": "Winter 1999",
        "filename": "newsletters/Winter_1999.pdf",
        "articles": '<p>"Maryland Handel Festival 2000, Schedule," 1, 6.</p><p>Traver, Paul. "Handel: Great Among the Nations," 1, 3.</p>',
    },
    {
        "id": "1999_summer",
        "friendly_name": "Summer 1999",
        "filename": "newsletters/Summer_1999.pdf",
        "articles": 'King, Richard G. "On Princess Anne\'s Patronage of the Second Academy," 1, 6.',
    },
    {
        "id": "1998_winter",
        "friendly_name": "Winter 1998",
        "filename": "newsletters/Winter_1998.pdf",
        "articles": '<p>Hunter, David. "Handel, John Hughes and Mary, Countess Cowper," 1, 6.</p><p>"1998 Maryland Handel Festival and American Handel Society Conference Abstracts," 3s–6.</p>',
    },
    {
        "id": "1998_summer",
        "friendly_name": "Summer 1998",
        "filename": "newsletters/Summer_1998.pdf",
        "articles": 'Beeks, Graydon. "A Curious Handel Performance at Keynsham," 1, 6.',
    },
    {
        "id": "1998_spring",
        "friendly_name": "Spring 1998",
        "filename": "newsletters/Spring_1998.pdf",
        "articles": '"The Hero in Drag: Omphale, Dejanira, and the Emasculization of Hercules," 1, 6.',
    },
    {
        "id": "1997_winter",
        "friendly_name": "Winter 1997",
        "filename": "newsletters/winter_1997.pdf",
        "articles": '<p>Hunter, David. "Advice to Mr. Handel," 3, 6.<p><p>Sadie, Julie Anne. "The Handel House Museum and the Byrne Collection," 1, 4–5.<p>',
    },
    {
        "id": "1997_summer",
        "friendly_name": "Summer 1997",
        "filename": "newsletters/Summer_1997.pdf",
        "articles": '<p>Facio, Iter. "The Handel Festivals in Göttingen (29 May to 2 June) and Halle 5 to 10 June)," 1, 3–4, 7.<p><p>Leissa, Brad. "High-Tech Handel," 1, 5.<p>',
    },
    {
        "id": "1997_spring",
        "friendly_name": "Spring 1997",
        "filename": "newsletters/Spring_1997.pdf",
        "articles": 'Beeks, Graydon. "More Handel Anthems in American Libraries," 1, 6.',
    },
    {
        "id": "1996_winter",
        "friendly_name": "Winter 1996",
        "filename": "newsletters/Winter_1996.pdf",
        "articles": '<p>"Abstracts of the 1996 American Handel Society Conference," 1, 3, 6.<p><p>Burrows, Donald. "Mr Handel\'s Friends: Contemporary Accounts of the Composer from the Papers of James Harris," 1, 4–6.<p>',
    },
    {
        "id": "1996_summer",
        "friendly_name": "Summer 1996",
        "filename": "newsletters/Summer_1996.pdf",
        "articles": '<p>Beeks, Graydon. "Handel and Lady Cobham," 1–2, 4.<p><p>Harris, Ellen T. "Handel on Stage," 1, 3–6.<p>',
    },
    {
        "id": "1996_spring",
        "friendly_name": "Spring 1996",
        "filename": "newsletters/Spring_1996.pdf",
        "articles": '<p>Harris, Ellen T. "Xerxes at Boston Lyric Opera, March 6–17, 1996," 1–2, 4.<p><p>Hunter, David. "The Oxford Musical Society\'s Manuscript of Handel\'s Coronation Anthems at Texas," 1, 3, 5.<p><p>Rosand, Ellen. "William Christie\'s Orlando at the Brooklyn Academy of Music February 9–13, 1996," 3.<p>',
    },
    {
        "id": "1995_winter",
        "friendly_name": "Winter 1995",
        "filename": "newsletters/Winter_1995.pdf",
        "articles": '<p>Beeks, Graydon. "Anna Strada del Pò: Handel\'s \'New\' Soprano," 3.</p><p>Beeks, Graydon. "Handel Queen Anne," 1, 6.</p><p>Fregosi, Bill. "Tamerlano at Glimmerglass," 1–2.</p><p>Lindgren, Lowell. "Joshua in Boston," 5</p>',
    },
    {
        "id": "1995_summer",
        "friendly_name": "Summer 1995",
        "filename": "newsletters/summer_1995.pdf",
        "articles": '<p>Auner, Joseph Henry. "Schoenberg and Handel in 1933," 1, 5–6.</p><p>Cervantes, Xavier. "Ezio in Paris," 7.</p><p>Facio, Iter. "The Forty-fourth Händel-Festspiele, Halle/Saale June 1995," 3, 9.</p><p>Harris, Ellen T. "Review of Farnelli," 1, 4.</p><p>Winemiller, John T. "Marcell\'s Bear and a St. Paul Alcina," 2, 8.</p>',
    },
    {
        "id": "1995_spring",
        "friendly_name": "Spring 1995",
        "filename": "newsletters/Spring_1995.pdf",
        "articles": '<p>Dean, Winton. "1994 American Handel Society Lecture: Handel\'s Operas in the Theater," 1–2.</p><p>Corn, Michael. "The Intellectual Context of Handel\'s Solomon," 1, 3–5.</p>',
    },
    {
        "id": "1994_winter",
        "friendly_name": "Winter 1994",
        "filename": "newsletters/Winter_1994.pdf",
        "articles": '<p>Perez, Karen, and Graydon Beeks. "Madame Melba Sings Handel," 1–2, 7.</p><p>"1994 American Handel Society Conference Abstracts," 3–6.</p>',
    },
    {
        "id": "1994_summer",
        "friendly_name": "Summer 1994",
        "filename": "newsletters/summer_1994.pdf",
        "articles": '<p>Facio, Iter. "Report from Halle," 1, 3.</p><p>Gossmann, Otto. "Report from Göttingen," 1, 4.</p>',
    },
    {
        "id": "1994_spring",
        "friendly_name": "Spring 1994",
        "filename": "newsletters/Spring_1994.pdf",
        "articles": '<p>Bennett, Shelley M. "Roubiliac\'s Handel," 1, 4.</p><p>Cervantes, Xavier. "Report from Montpellier," 5.</p><p>Facio, Iter. "Report form Karlsruhe," 1, 4. </p>',
    },
    {
        "id": "1993_winter",
        "friendly_name": "Winter 1993",
        "filename": "newsletters/winter_1993.pdf",
        "articles": '<p>Baselt, Bernd. "Handel\'s Oboe Concerto HWV 287: Contemporary Manuscript Source Rediscovered," 4.</p><p>Cervantes, Xavier. "Report from Montpellier," 4.</p><p>Facio, Iter. "Report from London," 1, 3.</p><p>Fleischhauer, Günter. "Professor Dr. phil, habil. Bernd Baselt (1934–1993): In memoriam," 1–2.</p>',
    },
    {
        "id": "1993_summer",
        "friendly_name": "Summer 1993",
        "filename": "newsletters/Summer_1993.pdf",
        "articles": '<p>Beeks, Graydon. "Handelian Keyboards," 1, 9.</p><p>Corneilson, Paul. "Mozart, Vogler, and Messiah," 2–3.</p><p>Facio, Iter. "Report from Germany," 1, 6–8.</p><p>Winemiller, John T. "Borrowing, Copyright, and Proprietary Authorship," 4–5.</p>',
    },
    {
        "id": "1993_spring",
        "friendly_name": "Spring 1993",
        "filename": "newsletters/Spring_1993.pdf",
        "articles": '<p>Mann, Alfred. "In Memoriam: Walther Siegmund-Schultze," 2.</p><p>Roberts, John H. "1992 American Handel Society Lecture: \'The Song for St. Cecilia\'s Day and Handel\'s Borrowing from Other Composers,\'" 1, 5.</p><p>Serwer, Howard, and Paul Traver. "J. Merrill Knapp 1914–1993," 1–2, 5.</p>',
    },
    {
        "id": "1992_winter",
        "friendly_name": "Winter 1992",
        "filename": "newsletters/Winter_1992.pdf",
        "articles": '<p>"Abstracts of the 1992 American Handel Society Conference," 3–6.</p><p>Beeks, Graydon. "Chichester Exhibition," 1, 7</p><p>McGegan, Nicholas. Book Review of Patrick J. Rogers, Contiuo Realization in Handel\'s Vocal Music (Ann Arbor, 1988), 2.</p>',
    },
    {
        "id": "1992_summer",
        "friendly_name": "Summer 1992",
        "filename": "newsletters/Summer_1992.pdf",
        "articles": '<p>Beeks, Graydon. "Göttingen 1992," 2.</p><p>Facio, Iter. "Halle 1992," 1, 5.</p><p>King, Richard G. "On Princess Anne\'s Lessons with Handel," 1, 4.</p>',
    },
    {
        "id": "1992_spring",
        "friendly_name": "Spring 1992",
        "filename": "newsletters/Spring_1992.pdf",
        "articles": '<p>Beeks, Graydon. "Messiah Anniversary: Some Further Thoughts," 1, 4.</p><p>Brainard, Paul. "Abstract of the 1991 American Handel Society Lecture: \'Bach and Handel: Another Look,\'" 2, 8.</p><p>Rogers, Patrick J. "Book Review of David Ledbetter, Continuo Playing According to Handel: His Figured Bass Exercises (Oxford, 1990)," 2, 5–6.</p><p>Serwer, Howard. "Agrippina," 1, 4–5.</p>',
    },
    {
        "id": "1991_winter",
        "friendly_name": "Winter 1991",
        "filename": "newsletters/Winter_1991.pdf",
        "articles": "",
    },
    {
        "id": "1991_summer",
        "friendly_name": "Summer 1991",
        "filename": "newsletters/Summer_1991.pdf",
        "articles": "",
    },
    {
        "id": "1991_spring",
        "friendly_name": "Spring 1991",
        "filename": "newsletters/Spring_1991.pdf",
        "articles": 'Olbrych, Judith Connor. "Handel in Dwight\'s Journal of Music," 1, 6–7.',
    },
    {
        "id": "1990_winter",
        "friendly_name": "Winter 1990",
        "filename": "newsletters/Winter_1990.pdf",
        "articles": "",
    },
    {
        "id": "1990_summer",
        "friendly_name": "Summer 1990",
        "filename": "newsletters/Summer_1990.pdf",
        "articles": "",
    },
    {
        "id": "1990_spring",
        "friendly_name": "Spring 1990",
        "filename": "newsletters/Spring_1990.pdf",
        "articles": "",
    },
    {
        "id": "1989_winter",
        "friendly_name": "Winter 1989",
        "filename": "newsletters/Winter_1989.pdf",
        "articles": "",
    },
    {
        "id": "1989_summer",
        "friendly_name": "Summer 1989",
        "filename": "newsletters/Summer_1989.pdf",
        "articles": "",
    },
    {
        "id": "1989_spring",
        "friendly_name": "Spring 1989",
        "filename": "newsletters/Spring_1989.pdf",
        "articles": "",
    },
    {
        "id": "1988_summer",
        "friendly_name": "Summer 1988",
        "filename": "newsletters/summer_1988.pdf",
        "articles": "",
    },
    {
        "id": "1988_spring",
        "friendly_name": "Spring 1988",
        "filename": "newsletters/Spring_1988.pdf",
        "articles": "",
    },
    {
        "id": "1987_winter",
        "friendly_name": "Winter 1987",
        "filename": "newsletters/Winter_1987.pdf",
        "articles": "",
    },
    {
        "id": "1987_summer",
        "friendly_name": "Summer 1987",
        "filename": "newsletters/Summer_1987.pdf",
        "articles": "",
    },
    {
        "id": "1987_spring",
        "friendly_name": "Spring 1987",
        "filename": "newsletters/Spring_1987.pdf",
        "articles": "",
    },
    {
        "id": "1986_winter",
        "friendly_name": "Winter 1986",
        "filename": "newsletters/Winter_1986.pdf",
        "articles": "",
    },
    {
        "id": "1986_summer",
        "friendly_name": "Summer 1986",
        "filename": "newsletters/Summer_1986.pdf",
        "articles": "",
    },
    {
        "id": "1986_spring",
        "friendly_name": "Spring 1986",
        "filename": "newsletters/Spring_1986.pdf",
        "articles": "",
    },
]
