import json
from bs4 import BeautifulSoup
import requests
import csv
import os
import settings
import constants
from pprint import pprint
from multiprocessing import Pool


def main():
    current_dir = os.path.dirname(__file__)
    relative_fandom_folder_path = os.path.join(current_dir, settings.fandom_page) + "/"

    with open(relative_fandom_folder_path + "pages.json", "r") as file:
        data = json.loads(file.read())

    with open(relative_fandom_folder_path + "pages_mapping.json", "r") as file:
        mapping = json.loads(file.read())

    processed_data = process_data_to_links(data)

    ids_mapped = map_ids(processed_data, mapping)

    with open(
        relative_fandom_folder_path + f"{settings.fandom_page}_page_links.csv", "w"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=ids_mapped[0].keys())
        writer.writeheader()
        writer.writerows(ids_mapped)


def map_ids(data, mapping):
    ids_mapped = []
    for i, object in enumerate(data):
        for link in object["links"]:
            p1id = i
            try:
                p2id = mapping[link]
            except KeyError:
                if ":" in link:
                    continue
                response = requests.get(link)
                link = response.url.split("#")[0]
                p2id = mapping[link]
            ids_mapped.append({"p1id": p1id, "p2id": p2id, "domain": object["domain"]})
    return ids_mapped


def process_data_to_links(data):
    with Pool(250) as p:
        processed_data = p.map(create_links_from_object, data)
    return processed_data
    # for object in data:
    #     links = create_links_from_object(object)
    #     object["links"] = links


def create_links_from_object(object):
    url = object["url"]
    title = object["name"]
    anchors = find_links_from_url(url)
    print(title, f"{len(anchors)}")
    links = set()
    for anchor in anchors:
        href = anchor.get("href")
        if not href or "https" in href:
            continue
        href = "https://" + constants.domain + href
        link = href.split("#")[0]
        links.add(link)
    links = list(links)
    return {"links": links, "domain": object["domain"]}


def find_links_from_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    main = soup.find("main")
    anchors = main.find_all("a")
    return anchors


if __name__ == "__main__":
    main()
