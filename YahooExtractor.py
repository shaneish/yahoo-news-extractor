    import requests
    import datetime as dt
    from tqdm.auto import tqdm
    import newspaper
    from newspaper import Article
    import pandas as pd
    import re

    def date_ish(date, add_days):
        new_date = date + dt.timedelta(add_days)
        day = str(new_date.day)
        month = str(new_date.month)
        if len(day)==1:
            day = "0" + day
        if len(month)==1:
            month = "0" + month
        return f"{new_date.year}{month}{day}"


    def get_yahoo_articles(subj="politics", date=None, date_range=1, return_archived=True, verbose=False):
        base = "https://news.yahoo.com/"
        if date is None:  date = dt.date.today()
        if type(date_range)!=int:
            date_range = (date_range - date).days
        days = [date_ish(date, day) for day in range(date_range)]
        links = set()
        for day in tqdm(days, disable=(not verbose)):
            arts = requests.get(f"https://web.archive.org/web/{day}/{base}/{subj}/")
            if arts.status_code==200:
                for token in arts.text.split(" "):
                    if return_archived:
                        search = re.findall('href="/web/\d+/http[s]?://news\.yahoo\.com(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.html"', token)
                    else:
                        search = re.findall('http[s]?://news\.yahoo\.com(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.html', token)
                    if len(search)>0:
                        if return_archived:
                            search = "https://web.archive.org" + search[0][6:-1]
                        else: search = search[0]
                        links.add(search)
        return list(links)

    def str_to_dt(dt):
        return dt.datetime.strptime(dt.split("+")[0], '%Y-%m-%d %H:%M:%S')

    def process_url(url):
        if 'operation-cobra-untold' in url:
            return ["", "", "", "", "", "", ""]
        art_data = []
        art = Article(url)
        try:
            art.download()
            art.parse()
            art_data.append(art.title)
            art_data.append(",".join(art.authors))
            art_data.append(str(art.publish_date).split("+")[0])
            art_data.append(art.text)
            art_data.append(art.summary)
            art_data.append(",".join(art.keywords))
            art_data.append(url)
            return art_data
        except:
            return ["", "", "", "", "", "", url]


def url_to_df(url_list, verbose=False):
    return pd.DataFrame([process_url(url) for url in tqdm(url_list, disable=(not verbose))], columns=['title', 'authors', 'datetime', 'text', 'summary', 'keywords', 'url'])

prez_list = ['Sanders', 'Bernie', 'Biden', 'Warren', 'Yang', 'Buttigieg', 'Gabbard', 'Booker', 'Castro', 'Steyer']

if __name__=="__main__":

    initial = True
    for month in range(1, 12):
        print(f'Month: {month}')
        yahoo_articles = get_yahoo_articles(date=dt.date(2019,month,1), date_range=dt.date(2019,month+1,1), verbose=True)
        df = url_to_df(yahoo_articles, verbose=True)
        df.to_csv("News.csv", mode='a', index=False, header=initial)
        initial = False

    yahoo_articles = get_yahoo_articles(date=dt.date(2019, 12, 1), date_range=dt.date(2019, 12, 15), verbose=True)
    df = url_to_df(yahoo_articles, verbose=True)
    df.to_csv("News.csv", mode='a', index=False, header=False)

    for month in range(1,2):
        yahoo_articles = get_yahoo_articles(date=dt.date(2018, 10+month, 1), date_range=dt.date(2018, 11+month, 1), verbose=True)
        df = url_to_df(yahoo_articles, verbose=True)
        df.to_csv("News.csv", mode='a', index=False, header=False)