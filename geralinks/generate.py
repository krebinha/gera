from bs4 import BeautifulSoup
from datetime import datetime
import requests
import codecs


def get_links() -> list[str]:
    site = "https://geralinks.com.br"
    soup = BeautifulSoup(requests.get(site).text, "html.parser")

    return list(set([
        (x.parent["title"], x.parent["href"], x["src"].split("src=")[-1])
        for x in soup.select("""a[href*="/link/"][title] > img""")
    ]))


def get_actual_link(link: str) -> str:
    soup = BeautifulSoup(requests.get(link).text, "html.parser")
    url = soup.select_one("""link[rel="dns-prefetch"][href]""")["href"]
    return url


def generate_rss_from_posts(posts: tuple[str, str, str, datetime]) -> str:
    rss = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    rss += '<rss version="2.0">\n'
    rss += '<channel>\n'
    rss += '\t<title>Geralinks Blog Posts - RSS Feed</title>\n'
    rss += '\t<link>https://github.com/ArjixGamer/anime-rss</link>\n'
    rss += '\t<description>A simple RSS feed for gogoanime!</description>\n\n\n'  # noqa

    for (title, link, image, date) in posts:
        rss += "\t<item>"
        rss += "\t\t<title>" + title + "</title>\n"
        rss += "\t\t<link>" + link + "</link>\n"
        rss += "\t\t<description>" + f'&lt;img src="{image}"&gt;' + "</description>\n"  # noqa
        rss += "\t</item>\n"

    rss += '\n</channel>\n</rss>'
    return rss


posts = sorted([
        (
            title, get_actual_link(link), img,
            datetime.fromisoformat("-".join(img.split("/")[-4:-1]))
        )
        for (title, link, img) in get_links()
    ],
    key=lambda x: x[3],
    reverse=True
)


with codecs.open("geralinks-feed.xml", "w", "utf-8") as f:
    f.write(generate_rss_from_posts(posts))
