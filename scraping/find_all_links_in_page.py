import json
from bs4 import BeautifulSoup
import requests
import csv
import os
from pprint import pprint
from multiprocessing import Pool


def main(fandom_page):
    current_dir = os.path.dirname(__file__)
    relative_fandom_folder_path = os.path.join(current_dir, fandom_page) + "/"

    with open(relative_fandom_folder_path + "pages.json", "r") as file:
        data = json.loads(file.read())

    with open(relative_fandom_folder_path + "pages_mapping.json", "r") as file:
        mapping = json.loads(file.read())

    add_links_to_objects(data)

    ids_mapped = map_ids(data, mapping)

    with open(relative_fandom_folder_path + f"edges.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=ids_mapped[0].keys())
        # writer.writeheader()
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
            ids_mapped.append(
                {
                    ":START_ID": p1id,
                    "weight": 1,
                    ":END_ID": p2id,
                    ":TYPE": "HAS_LINK_TO",
                }
            )
    return ids_mapped


def add_links_to_objects(data):
    with Pool(50) as p:
        data[:] = p.map(process_object, data)

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
        href = "https://" + object[":LABEL"] + href
        link = href.split("#")[0]
        links.add(link)
    links = list(links)
    return links


def find_links_from_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    main = soup.find("main")
    anchors = main.find_all("a")
    return anchors


def process_object(object):
    object["links"] = create_links_from_object(object)
    return object


if __name__ == "__main__":
    main()
