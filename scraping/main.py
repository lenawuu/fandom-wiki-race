import find_all_pages
import find_all_links_in_page
import settings
import os
import shutil


def main():
    for fandom_page in settings.fandom_pages:
        find_all_pages.main(fandom_page)
        find_all_links_in_page.main(fandom_page)

    current_dir = os.path.dirname(__file__)
    import_folder_path = os.path.join(current_dir, "import")

    initialize_import_folder(import_folder_path)
    create_headers(import_folder_path)

    for i, fandom_page in enumerate(settings.fandom_pages, start=1):
        fandom_folder_path = f"{current_dir}/{fandom_page}"
        shutil.move(
            f"{fandom_folder_path}/nodes.csv",
            f"{import_folder_path}/nodes-part{i}.csv",
        )
        shutil.move(
            f"{fandom_folder_path}/edges.csv",
            f"{import_folder_path}/edges-part{i}.csv",
        )

        shutil.rmtree(fandom_folder_path)


def initialize_import_folder(import_folder_path):
    if os.path.exists(import_folder_path):
        shutil.rmtree(import_folder_path)
    os.makedirs(import_folder_path)


def create_headers(import_folder_path):
    with open(f"{import_folder_path}/edges-header.csv", "w") as f:
        f.write(":START_ID,weight,:END_ID,:TYPE")

    with open(f"{import_folder_path}/nodes-header.csv", "w") as f:
        f.write("pageId:ID,name,url,:LABEL")


if __name__ == "__main__":
    main()
