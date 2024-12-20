from bs4 import BeautifulSoup, Tag
import csv
import json
import os
import requests
import shutil
import utils
import settings


def main(fandom_page_name):
    links = generate_links(fandom_page_name)

    objects = list(map(lambda link: link.get_object(), links))

    current_dir = os.path.dirname(__file__)
    relative_fandom_folder_path = os.path.join(current_dir, fandom_page_name)
    if os.path.exists(relative_fandom_folder_path):
        shutil.rmtree(relative_fandom_folder_path)
    os.makedirs(relative_fandom_folder_path)

    relative_fandom_folder_path += "/"

    with open(relative_fandom_folder_path + "pages.json", "w") as file:
        json.dump(objects, file)

    mapping = {}
    for object in objects:
        mapping[object["url"]] = object["pageId:ID"]

    with open(relative_fandom_folder_path + "pages_mapping.json", "w") as file:
        json.dump(mapping, file)

    with open(relative_fandom_folder_path + f"nodes.csv", "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=objects[0].keys())
        # writer.writeheader()
        writer.writerows(objects)


class WikiPage:
    current_id = settings.starting_index

    def __init__(self, name, url, fandom_page) -> None:
        self.domain = utils.get_domain(fandom_page)
        self.name = name
        self.url = url
        self.id = WikiPage.current_id
        WikiPage.current_id += 1

    def get_object(self):
        return {
            "pageId:ID": self.id,
            "name": self.name,
            "url": "https://" + self.domain + self.url,
            ":LABEL": self.domain,
        }


def extract_pages_from_chunk(all_pages_chunk: Tag, fandom_page) -> list[WikiPage]:
    tags = all_pages_chunk.find_all("a")
    good_tags = filter(lambda tag: "class" not in tag.attrs, tags)
    links = map(
        lambda tag: WikiPage(tag.get("title"), tag.get("href"), fandom_page), good_tags
    )
    return list(links)


def generate_links(fandom_page):
    links = []
    domain = utils.get_domain(fandom_page)
    current_url = "https://" + domain + "/wiki/Special:AllPages"
    while current_url:
        print(current_url)
        page = requests.get(current_url)
        soup = BeautifulSoup(page.content, "html.parser")
        chunk = soup.find("ul", class_="mw-allpages-chunk")
        links.extend(extract_pages_from_chunk(chunk, fandom_page))
        current_url = next_nav_url(soup, fandom_page)
    return links


def next_nav_url(soup: BeautifulSoup, fandom_page) -> str:
    nav = soup.find("div", class_="mw-allpages-nav")
    if not nav:
        return None
    a = nav.findChildren("a")[-1]
    if "next page" not in a.text.lower():
        return None
    return "https://" + utils.get_domain(fandom_page) + a.get("href")


if __name__ == "__main__":
    main()
