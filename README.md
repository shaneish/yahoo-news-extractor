# yahoo-news-extractor

Quick script to pull and scrape old Yahoo Political News articles for a project to look at whether there really is a "Bernie Blackout" or not.  

YahooExtractor.py is a quick script (largely uncommented, I just wanted the data) that pulls the articles from archived Yahoo News! Politics pages and YahooCleaner.ipynb is an ugly notebook (seriously, it's just a scrap book--it doesn't look pretty) I used to clean the data.  Punctuation, casing, and excess whitespaces was stripped from text but words were left un-lemmatized to give a bit of play with the lemmatization process when I'm actually analyzing the data.

RawNews.csv is the raw output .csv from the script and CleanedNew.csv is the cleaned dataset I'll be using for the project.
