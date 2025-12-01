from django.templatetags.static import static

ZEFFY_EMBED_URL_FOR_RENEWAL_FORM = (
    "https://www.zeffy.com/embed/ticketing/membership-renewal-3"
)

RESEARCH_MATERIALS = {
    "open_source": [
        {
            "title": "Bibliothekssystem Universität Hamburg",
            "url": "https://digitalisate.sub.uni-hamburg.de/",
            "description": "Includes some digitized Handel conducting scores.",
        },
        {
            "title": "British Library Digitised Manuscripts",
            "url": "https://www.bl.uk/collection/digitised-manuscripts-archives",
            "description": "The British Library hosts digitized copies of most of Handel's autograph manuscripts available for free through their online catalog",
        },
        {
            "title": "Concert Programmes",
            "url": "http://www.concertprogrammes.org.uk/",
            "description": "A database of collections of concert programs held in European libraries, archives, and museums. ",
        },
        {
            "title": "Corago",
            "url": "http://corago.unibo.it/",
            "description": "A database of Italian operas and opera librettos 1600–1900 with links to digital copies of opera librettos.",
        },
        {
            "title": "English Short Title Catalogue",
            "url": "http://estc.bl.uk/F/?func=file&file_name=login-bl-estc",
            "description": "A database of works published in the British Isles and North America between 1473 and 1800. Helpful in locating printed Handel wordbooks (including digitized copies) in libraries all over the world.",
        },
        {
            "title": "Gallica ",
            "url": "https://gallica.bnf.fr/accueil/en/content/accueil-en?mode=desktop ",
            "description": "Digital library created by the Bibliothèque nationale de France and its partner institutions. Millions of documents are available online including newspapers, manuscripts, musical scores, images, and books.",
        },
        {
            "title": "Gerald Coke Handel Collection   ",
            "url": "https://foundling.soutron.net/Portal/Default/en-GB/Search/SimpleSearch ",
            "description": "A collection of books, journals, manuscripts, printed music, libretti, ephemera, sound recordings, artworks, archives, and artefacts relating to Handel and his circle. Some items have been digitized.",
        },
        {
            "title": "Google Books ",
            "url": "https://books.google.com/advanced_book_search",
            "description": "Particularly useful is the full-text search of out-of-copyright books, including some librettos.    ",
        },
        {
            "title": "Händel-Haus Collections",
            "url": "https://kxp.k10plus.de/DB=9.444/",
            "description": "Includes digitized early printed editions of Handel by John Walsh, portraits of Handel, and other paintings and art relating to Handel. ",
        },
        {
            "title": "Handel and Haydn Society (H+H) Digital Archive",
            "url": "https://handelandhaydn.access.preservica.com",
            "description": "An archive of more than 1,000 H+H concert program books going back to July 1818, containing records of Handel's works performed in America.",
        },
        {
            "title": "Handel Opera Performances Since 1705",
            "url": "https://haendelhaus.de/en/opernauffuehrung",
            "description": "A database of performances of Handel's music dramas in staged productions or concert performances since 1705 (including concert performances of operas but not including oratorio concerts).",
        },
        {
            "title": "Handel Reference Database",
            "url": "http://ichriss.ccarh.org/HRD/",
            "description": "A database containing transcribed letters, newspaper articles, and other documents related to Handel organized by year.",
        },
        {
            "title": "HathiTrust Digital Library",
            "url": "https://www.hathitrust.org/",
            "description": "Contains digitized images of various Handel scores and books on Handel.",
        },
        {
            "title": "IMSLP Petrucci Music Library",
            "url": "https://imslp.org/wiki/Main_Page",
            "description": "List of digitized Handel scores.",
        },
        {
            "title": "Internet Archive",
            "url": "https://archive.org/",
            "description": "List of digitized Handel resources (books, scores, librettos, etc.)",
        },
        {
            "title": "Internet Culturale",
            "url": "https://www.internetculturale.it/",
            "description": "Catalog and digital collection of Italian libraries; contains many digitized manuscripts and printed sources in Italian.",
        },
        {
            "title": "James S. Hall Collection of George Frideric Handel at Princeton University",
            "url": "https://dpul.princeton.edu/music/catalog?f%5Breadonly_collections_ssim%5D%5B%5D=James+S.+Hall+collection+of+George+Frideric+Handel&search_field=all_fields",
            "description": "Some items in this collection have been digitized.",
        },
        {
            "title": "Jisc Library Hub Discover",
            "url": "https://discover.libraryhub.jisc.ac.uk/",
            "description": "A database of catalogs of major UK and Irish libraries with links to digitized documents.",
        },
        {
            "title": "Karlsruhe Virtual Catalog",
            "url": "https://kvk.bibliothek.kit.edu/?digitalOnly=0&embedFulltitle=0&newTab=0",
            "description": "A meta search engine for the identification of several hundred million media in libraries and book catalogs worldwide (national libraries, union catalogs, collections, and digital-media-only sites, including Hathi Trust, Internet Archive, and others).",
        },
        {
            "title": "The Librettos of Handel's Operas",
            "url": "https://catalog.hathitrust.org/Record/001098579/Home",
            "description": "A digitized collection of seventy-one opera librettos.",
        },
        {
            "title": "Libretto Portal",
            "url": "https://libretti.digitale-sammlungen.de//de/fs1/start/static.html",
            "description": "Offers access to two libretto collections which have been catalogued and digitized in Bayerische Staatsbibliothek and German Historical Institute in Rome.",
        },
        {
            "title": "Musiconn",
            "url": "https://scoresearch.musiconn.de/ScoreSearch/?lang=en",
            "description": "A program for finding sequence of notes in selected digitized music editions including works of Handel (Chrysander edition digitized in Münchener DigitalisierungsZentrum Digitale Bibliothek).",
        },
        {
            "title": "RISM",
            "url": "https://rism.info/",
            "description": "Online catalog of extant musical sources worldwide, primarily manuscripts and printed music editions, with many links to digitized copies.",
        },
        {
            "title": "Samuel Arnold Edition of Handel’s Works Digitized and Available Online",
            "url": "/static/Rogers_List_of_Arnold_Edition_of_Handels_Works.pdf",
            "description": "A resource compiled by Patrick Rogers.",
        },
        {
            "title": "University of North Texas Digital Library",
            "url": "https://digital.library.unt.edu/search/?q=george+frideric+handel&t=fulltext&fq=dc_type%3Aimage_score",
            "description": "Contains digitized early Handel scores.",
        },
    ],
    "subscription_based": [
        {
            "title": "Burney Collection of Newspapers",
            "url": "https://www.gale.com/c/seventeenth-and-eighteenth-century-burney-newspapers-collection",
            "description": "Searchable digitized database of the British Library's Burney Collection of 17th- and 18th-Century Newspapers.",
        },
        {
            "title": "Eighteenth Century Collections Online (ECCO)",
            "url": "https://www.gale.com/primary-sources/eighteenth-century-collections-online",
            "description": "Online archive of English-language and foreign-language titles printed in the British Isles, colonies, and the United States between the years 1701 and 1800.",
        },
        {
            "title": "Eighteenth Century Journals",
            "url": "https://www.18thcjournals.amdigital.co.uk/",
            "description": "Digitized collection of 18th-century journals in English.",
        },
    ],
}

BOARD_OF_DIRECTORS = [
    ("Graydon Beeks", "Ireri Chávez-Bárcenas"),
    ("Alison DeSimone", "Norbert Dubowy"),
    ("Fredric Fehleisen", "Roger Freitas"),
    ("Wendy Heller", "Robert Ketterer"),
    ("Minji Kim", "Nathan Link"),
    ("Ken Nott", "Marjorie Pomeroy"),
    ("Mark Risinger", "John Roberts"),
    ("Ayana Smith", ""),
]

HONORARY_DIRECTORS = [
    "William Gudger",
    "Ellen T. Harris",
    "David Hurley",
    "Richard King",
    "Nicholas McGegan",
    "Marty Ronish",
    "Ellen Rosand",
]

HOWARD_SERWER_LECTURES = [
    {
        "year": 2023,
        "speaker": "Nathan Link",
        "title": "Narrative and Drama in Handel's Operas",
        "location": "Bloomington, IN – Indiana University",
    },
    {
        "year": 2021,
        "speaker": "Berta Joncus",
        "title": "Posterity vs Celebrity: Handel Studies and the 21st Century",
        "location": "Virtual Conference – Hosted by Indiana University",
    },
    {
        "year": 2019,
        "speaker": "Ellen Rosand",
        "title": "Handel's 'Music'",
        "location": "Bloomington, IN – Indiana University",
    },
    {
        "year": 2017,
        "speaker": "John Butt",
        "title": "Handel and Messiah: Harmonizing the Bible for a Modern World?",
        "location": "Princeton, NJ – Princeton University",
    },
    {
        "year": 2015,
        "speaker": "Nicholas McGegan",
        "title": "Handel in My Lifetime",
        "location": "Iowa City, IA – University of Iowa",
    },
    {
        "year": 2013,
        "speaker": "Reinhard Strohm",
        "title": "Handel: Opera and Ritual",
        "location": "Princeton, NJ – Princeton University",
    },
    {
        "year": 2011,
        "speaker": "David Hurley",
        "title": "Once More with Feeling: Da Capo Patterns in Handel's Oratorios",
        "location": "Seattle, WA",
    },
    {
        "year": 2009,
        "speaker": "Robert Ketterer",
        "title": "London as Athens: <em>Teseo</em> and <em>Arianna in Creta</em>",
        "location": "Danville, KY - Centre College",
    },
    {
        "year": 2007,
        "speaker": "Andrew Porter",
        "title": "How Handel's Operas Entered the Modern Repertory",
        "location": "Princeton, NJ – Princeton University",
    },
    {
        "year": 2005,
        "speaker": "Graydon Beeks",
        "title": "Private Patronage of Church Music in the Reign of George I",
        "location": "Santa Fe, NM",
    },
    {
        "year": 2003,
        "speaker": "Terence Best",
        "title": "Handel Editions",
        "location": "Iowa City, IA – University of Iowa",
    },
    {
        "year": 2001,
        "speaker": "Nicholas Temperley",
        "title": "'In Virtue's Cause': How Handel's Music was Sanctified",
        "location": "College Park, MD – University of Maryland",
    },
    {
        "year": 2000,
        "speaker": "Ruth Smith",
        "title": "Fifteen Ways to Skin an Oratorio, of Understanding <em>Theodora</em>",
        "location": "College Park, MD – University of Maryland",
    },
    {
        "year": 1998,
        "speaker": "Anthony Hicks",
        "title": "Handel's Jephtha: A Sacridice to Theology?",
        "location": "College Park, MD – University of Maryland",
    },
    {
        "year": 1996,
        "speaker": "Donald Burrows",
        "title": "M. Handel's Friends: Contemporary Accounts of the Composer from the papers of James T. ",
        "location": "College Park, MD – University of Maryland",
    },
    {
        "year": 1994,
        "speaker": "Winton Dean",
        "title": "Handel's Operas in the Theatre",
        "location": "College Park, MD – University of Maryland",
    },
    {
        "year": 1992,
        "speaker": "John Roberts",
        "title": "The <em>Song for St Cecilia's Day</em> and Handel's 'Borrowing' from other Composers",
        "location": "College Park, MD - University of Maryland",
    },
    {
        "year": 1991,
        "speaker": "Paul Brainard",
        "title": "Bach and Handel: Another Look",
        "location": "Washington, D.C. – George Washington University",
    },
    {
        "year": 1990,
        "speaker": "Don E. Saliers",
        "title": "Words and The Word: Sounding the Text of Handel's <em>Messiah</em>",
        "location": "College Park, MD – University of Maryland",
    },
    {
        "year": 1989,
        "speaker": "Bernd Baselt",
        "title": "The War of Spanish Succession, Italy, and Handel",
        "location": "College Park, MD – University of Maryland",
    },
    {
        "year": 1988,
        "speaker": "Ellen T. Harris",
        "title": "Integrity and Improvisation in the Music of Handel",
        "location": "College Park, MD – University of Maryland",
    },
    {
        "year": 1987,
        "speaker": "Jens Peter Larsen",
        "title": "The Turning Point in Handel's Oratorio Tradition",
        "location": "College Park, MD – University of Maryland",
    },
]

KNAPP_FELLOWSHIP_WINNERS = [
    {
        "year": 2024,
        "recipient": "Peter Kohanski",
        "affiliation": "University of  North Texas",
        "supported_research": 'To support research at the Historical Society of Pennsylvania for his dissertation "Sounding Britain, Crafting Self: Handel, Imperial Identities, and Eighteenth-Century Lives of Empire."',
    },
    {
        "year": 2024,
        "recipient": "Paul Feller",
        "affiliation": "Northwestern University",
        "supported_research": "To support travel to the Ets Haim Library and the Stadsarchief in Amsterdam for his doctoral project on intersection between Handel's music and the Dutch Sephardic community.",
    },
    {
        "year": 2022,
        "recipient": "Blake Johnson",
        "affiliation": "University of Missouri-Kansas City Conservatory",
        "supported_research": "To support travel to London to conduct research at the British Library and the National Archives on the performance styles of foreign oboists in eighteenth-century London.",
    },
    {
        "year": 2020,
        "recipient": "Patrick Rogers",
        "affiliation": "Independent scholar",
        "supported_research": 'To support the cost of digital copies, interlibrary loans, and travel related to his project "Samuel Arnold as Editor and Performer of Handel’s Music."',
    },
    {
        "year": 2018,
        "recipient": "Alison DeSimone",
        "affiliation": "University of Missouri–Kansas City",
        "supported_research": 'To support a research trip to the United Kingdom for work on her monograph-in-progress, "The Power of Pastiche: Musical Miscellany and the Creation of Cultural Identity in Early Eighteenth-Century England."',
    },
    {
        "year": 2016,
        "recipient": "Carlo Lanfossi",
        "affiliation": "University of Pennsylvania ",
        "supported_research": 'To support travel to view <em>in situ</em> the sources of numerous pasticci involving Handel in some way for his project "Handel as Arranger and Producer: Listening to Pasticci in Eighteenth-Century London."',
    },
    {
        "year": 2016,
        "recipient": "Matthew Gardner",
        "affiliation": "Goethe-Universität, Frankfurt am Main",
        "supported_research": "To support travel to view <em>in situ</em> sources of the oratorio <em>Deborah</em> as he prepares the critical edition for the Hallische Händel-Ausgabe.",
    },
    {
        "year": 2012,
        "recipient": "Regina Compton",
        "affiliation": "Eastman School of Music",
        "supported_research": "To support travel to London to conduct research for her dissertation on the <em>recitativo semplice</em> in Handel's Academy operas.",
    },
    {
        "year": 2011,
        "recipient": "Alison Desimone",
        "affiliation": "University of Michigan ",
        "supported_research": 'To support travel to London and Venice for the dissertation "Female Opera Singers and the Performance of Identity in Early Eighteenth-Century London."',
    },
    {
        "year": 2011,
        "recipient": "Andrew Woolley",
        "affiliation": "University of Southhampton ",
        "supported_research": 'To support travel to London, Cambridge and Chichester for the project "Research on the William Walond Manuscript of Keyboard Music in the Gerald Coke Handel Collection at the Foundling Museum Library, London, UK, and Related Sources."',
    },
    {
        "year": 2009,
        "recipient": "Thomas McGeary",
        "affiliation": "Independent scholar",
        "supported_research": 'To pay for the provision of numerous illustrations for the 2009 essay in <em>Early Music</em>, "Handel as Art Collector: Art, Connoisseurship and Taste in Hanoverian Britain."',
    },
    {
        "year": 2005,
        "recipient": "Nathan Link",
        "affiliation": "Yale University",
        "supported_research": "To support travel to Hamburg to study the Handel's conducting scores at the Staats- und Universitätsbibliothek.",
    },
    {
        "year": 2004,
        "recipient": "Ilias Chrissochoidis",
        "affiliation": "Stanford University",
        "supported_research": "To support research on the political context of Handel's <em>Esther</em> in 1732.",
    },
    {
        "year": 2003,
        "recipient": "Zachariah Victor",
        "affiliation": "Yale University",
        "supported_research": 'To support work on "An Interdisciplinary Study of Vocal Genres and the Pastoral in the Music of Alessandro Scarlatti, 1693-1707," including connections between Handel and Scarlatti as cantata composers.',
    },
    {
        "year": 2002,
        "recipient": "Minji Kim",
        "affiliation": "Brandeis University",
        "supported_research": 'To support travel to London for research on the topic "Handel\'s <em>Israel in Egypt</em>: a Three-Anthem Oratorio."',
    },
    {
        "year": 2001,
        "recipient": "Major Peter C. Giotta (Asst. Professor of English)",
        "affiliation": "United States Military Academy (West Point)",
        "supported_research": "To support a research trip to England to explore how Handel's oratorio Samson affected the reception of Milton's poetry in the 18th century.",
    },
    {
        "year": 2000,
        "recipient": "Stanley Pelkey",
        "affiliation": "Gordon College",
        "supported_research": "To explore the the formation of canonical repertoires in Georgian Britain and the influence that those canons, and especially the music of Handel, had on compositional practices in the late eighteenth and early nineteenth centuries.",
    },
    {
        "year": 1999,
        "recipient": "Kenneth McLeod",
        "affiliation": "Massachusetts Institute of Technology",
        "supported_research": "To study sources for <em>Eccles'</em> and Handel's <em>Semele</em> in London to assist with the completion of his project, \"Masculine Anxiety in Handel's <em>Semele</em>.\"",
    },
    {
        "year": 1998,
        "recipient": "Todd Gilman",
        "affiliation": "Massachusetts Institute of Technology",
        "supported_research": "To study sources and materials by the English composer and Handel contemporary, Thomas Augustine Arne, at the Britten-Pears library in Aldeburth, England.",
    },
    {
        "year": 1996,
        "recipient": "Barbara Durost",
        "affiliation": "Claremont Graduate School",
        "supported_research": "To study manuscript sources of William Croft's works in England and to search for concordances in major collections of single songs and anthologies in English libraries, and thereby shed light in Handel's activities during the same period.",
    },
    {
        "year": 1995,
        "recipient": "Mark Risinger",
        "affiliation": "Harvard University",
        "supported_research": "To study Handel autographs in London and Cambridge, England.",
    },
    {
        "year": 1993,
        "recipient": "Michael Corn",
        "affiliation": "University of Illinois",
        "supported_research": "",
    },
    {
        "year": 1993,
        "recipient": "Channan Willner",
        "affiliation": "City University of New York",
        "supported_research": "To complete the recipient's dissertation on the analysis of Handel's music.",
    },
    {
        "year": 1991,
        "recipient": "John Winemiller",
        "affiliation": "University of Chicago",
        "supported_research": "To complete archival research on Handel's self-borrowings from his abandoned opera, <em>Titus</em> (1731/32) and thereby complete his dissertation, \"Aspects of neoclassicism in Handel's compositional aesthetic.\"",
    },
    {
        "year": 1990,
        "recipient": "Richard G. King",
        "affiliation": "Stanford University",
        "supported_research": "To study Handelian biographical archives in the Netherlands.",
    },
    {
        "year": 1989,
        "recipient": "David Ross Hurley ",
        "affiliation": "University of Chicago ",
        "supported_research": "To complete the recipient's dissertation: \"Handel's Compositional Process: A Study of Selected Oratorios.\"",
    },
]


BOSTON_25_AGENDA = [
    # Thursday
    {
        "date": "Thursday, February 6</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "6:00pm",
        "description": "Opening Reception",
    },
    {
        "date": "Thursday, February 6</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "6:45pm",
        "description": "Welcome—Graydon Beeks, President, American Handel Society",
    },
    {
        "date": "Thursday, February 6</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "6:50pm",
        "description": "<h3 class='tr-header'>Howard Serwer Memorial Lecture</h3></strong><p><em>Chair, Graydon Beeks</em></p><p>Ayana Smith (Indiana University, Jacobs School of Music), \"Deathly Images: Discourses of Sight and Sound in Handel's London Operas\"</p>",
    },
    # Friday
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "7:50am",
        "description": "Bus 1 leaves The Colonnade for MIT",
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "8:15am",
        "description": "Bus 2 leaves The Colonnade for MIT",
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "8:30am",
        "description": '<i class="fa-solid fa-utensils"></i> Breakfast',
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "9:00am",
        "description": '<i class="fa-solid fa-hands-clapping"></i> Welcome — Ellen T. Harris, Chair, Local Arrangements',
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "",
        "description": "<h3 class='tr-header'>Paper Session 1</h3><p><em>Chair, Mark Risinger</em></p><p>Bells and Whistles: Handel's Sounds of Love and Madness </p>",
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "9:10am",
        "description": "Minji Kim (American Handel Society), \"'Make poor Saul stark mad': Sonic Effect of Bells in Handel's <em>Saul</em>\"",
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "9:50am",
        "description": "Blake Johnson (Campbellsville University), \"'Where Love or Honour Calls': The Role of the Oboe in Handel's Early Operas, 1705–15\"",
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "10:20am",
        "description": '<i class="fa-solid fa-mug-hot"></i> Coffee break',
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "",
        "description": "<h3 class='tr-header'>Paper Session 2</h3><p><em>Chair, Mark Risinger</em></p><p>Handelian Encounters</p>",
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "10:40am",
        "description": 'Ruth Eldredge Thomas (Durham University), "Bach, Handel, and Religion in the English Nineteenth Century"',
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "11:20am",
        "description": "Kenneth Nott (The Hartt School), \"Lou Harrison and 'The Divine Mr. Handel'\"",
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "12:15pm",
        "description": f"<h3 class='tr-header'>Paul Traver Memorial Concert</h3>Singers of MIT Chamber Chorus and soloists from Emmanuel Music, conducted by Ryan Turner, will perform Handel's first setting of \"As pants the hart\" and other works by Victoria and Palestrina.</p><p>Free admission.</p><p>Thomas Tull Concert Hall, Linde Music Building, MIT</p><p><a href={static('2025_Paul_Traver_Memorial_Concert.pdf')} target='_blank'><i class='fas fa-download' aria-hidden='true'></i> Download program</a></p>",
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "1:00pm",
        "description": '<i class="fa-solid fa-utensils"></i> Lunch',
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "",
        "description": "<h3 class='tr-header'>Paper Session 3</h3><p><em>Chair, Wendy Heller</em></p><p>Handel in America</p>",
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "2:30pm",
        "description": 'Joe Lockwood (Newcastle University), "<em>Zadok the Priest</em>, the “Hallelujah!” Chorus, and the Imperial Soundscape in Boston on the Brink of Revolution"',
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "3:10pm",
        "description": 'Berta Joncus (Guildhall School of Music & Drama), "Handel Melodies and Anti-Slavery Activism: Music for the Common Good"',
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "3:50pm",
        "description": '<i class="fa-solid fa-mug-hot"></i> Coffee break',
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "4:10pm",
        "location": "Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "description": 'Stephen Nissenbaum (Underhill, VT), "From Göttingen to Northampton: Handel Operas Arrive in America, 1927–1931"',
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "5:00pm",
        "description": "Bus 1 leaves MIT for The Colonnade",
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "5:30pm",
        "description": "Bus 2 leaves MIT for The Colonnade",
    },
    {
        "date": "Friday, February 7</br>Erdely Music & Culture Space, Linde Music Building, Massachusetts Institute of Technology (201 Amherst Street, Cambridge)",
        "time": "7:30pm",
        "location": "Jordan Hall, New England Conservatory (30 Gainsborough Street)",
        "description": "<h3 class='tr-header'>Concert</h3><p>Joélle Harvey (soprano) and the Handel + Haydn Society, conducted by Jonathan Cohen.</p><p>Jordan Hall, New England Conservatory (30 Gainsborough Street)</p>",
    },
    # Saturday
    {
        "date": "Saturday, February 8</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "8:30am",
        "description": '<i class="fa-solid fa-utensils"></i> Breakfast',
    },
    {
        "date": "Saturday, February 8</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "",
        "description": "<h3 class='tr-header'>Paper Session 4</h3><p><em>Chair, Robert Ketterer</em></p><p>Reconstructions</p>",
    },
    {
        "date": "Saturday, February 8</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "9:15am",
        "description": 'Graydon Beeks (Pomona College)<p>"Sir Watkin Williams Wynn, 4th Bart. (1749–1789) as a Collector of Handel\'s Music"</p>',
    },
    {
        "date": "Saturday, February 8</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "9:55am",
        "description": "Alexander McCargar (University of Vienna), \"Johann Oswald Harms and Handel's 'Lost' Nero\"",
    },
    {
        "date": "Saturday, February 8</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "10:35am",
        "description": '<i class="fa-solid fa-mug-hot"></i> Coffee break',
    },
    {
        "date": "Saturday, February 8</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "10:55am",
        "description": "Ruth Smith (The Handel Institute), \"Handel's <em>Solomon</em> and Solomon's Temple\"",
    },
    {
        "date": "Saturday, February 8</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "12:00pm",
        "description": '<i class="fa-solid fa-utensils"></i> Lunch / AHS Board Meeting (College Club)',
    },
    {
        "date": "Saturday, February 8</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "",
        "description": "<h3 class='tr-header'>Paper Session 5</h3><p><em>Chair, Berta Joncus</em></p><p>Oratorios: From Composer to Editor</p>",
    },
    {
        "date": "Saturday, February 8</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "2:00pm",
        "description": 'Fred Fehleisen (The Juilliard School), "Handel\'s First Day on the Job: 22 August 1741"',
    },
    {
        "date": "Saturday, February 8</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "2:40pm",
        "description": 'Mark Risinger (New York, NY), "On the Rhetorical Structure and Function of Handel\'s Oratorio Choruses"',
    },
    {
        "date": "Saturday, February 8</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "3:20pm",
        "description": '<i class="fa-solid fa-mug-hot"></i> Coffee break',
    },
    {
        "date": "Saturday, February 8</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "3:40pm",
        "description": 'Annette Landgraf (Hallische Händel-Ausgabe), "The Different Historical Editions of <em>Judas Maccabaeus</em> and Challenges for a Modern Edition"',
    },
    {
        "date": "Saturday, February 8</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "4:20pm",
        "description": "Donald Burrows (Open University), \"'In the manner of an oratorio': Interpreting the Bottom Stave in Handel's Score of <em>Messiah</em>\"",
    },
    {
        "date": "Saturday, February 8</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "8:00pm",
        "location": "First Lutheran Church, Boston (299 Berkeley Street)",
        "description": "<h3 class='tr-header'>Concert</h3><p>Francesco Corti, harpsichord and organ, joins the Boston Early Music Festival Chamber Ensemble and director Robert Mealy.</p><p>First Lutheran Church, Boston (299 Berkeley Street)</p>",
    },
    # Sunday
    {
        "date": "Sunday, February 9</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "8:30am",
        "description": '<i class="fa-solid fa-utensils"></i> Breakfast',
    },
    {
        "date": "Sunday, February 9</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "9:00am",
        "description": "Open Business Meeting",
    },
    {
        "date": "Sunday, February 9</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "",
        "description": "<h3 class='tr-header'>Paper Session 6</h3><p><em>Chair, Nathan Link</em></p><p>Competition, <em>Prime donne</em>, and Theatricality</p>",
    },
    {
        "date": "Sunday, February 9</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "9:30am",
        "description": 'Francesca Greppi (University of Bologna), "Soprano Pairing at the Teatro Grimani di San Giovanni Grisostomo in Venice: Bordoni and Cuzzoni\'s Early Collaborations in Italy"',
    },
    {
        "date": "Sunday, February 9</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "10:10am",
        "description": 'David Vickers (Royal Northern College of Music), "Giulia Frasi and Italian Music in London"',
    },
    {
        "date": "Sunday, February 9</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "10:50am",
        "description": '<i class="fa-solid fa-mug-hot"></i> Coffee break',
    },
    {
        "date": "Sunday, February 9</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "11:10am",
        "description": 'Yseult Martinez (Sorbonne University), "Female Cross-Dressing and Men\'s Redemption on the London Opera Stage: Handel and Transvestite Heroines during the 1730s"',
    },
    {
        "date": "Sunday, February 9</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "11:50pm",
        "description": 'Matthew Gardner (University of Tübingen), "Handel\'s Theatre Singers 1737–1741"',
    },
    {
        "date": "Sunday, February 9</br>College Club of Boston (44 Commonwealth Avenue)",
        "time": "12:30pm",
        "description": "<i class='fa-solid fa-hands-clapping'></i> Closing Remarks – Graydon Beeks",
    },
]
