import json
import os
from github import Github

# define a function to add a shoe to the collection
def add_shoe(collection, name, brand, size):
    shoe = {"name": name, "brand": brand, "size": size}
    collection.append(shoe)
    return collection

# define a function to save the collection to a JSON file
def save_collection(collection):
    with open("shoe_collection.json", "w") as f:
        json.dump(collection, f)

# define a function to load the collection from a JSON file
def load_collection():
    try:
        with open("shoe_collection.json", "r") as f:
            collection = json.load(f)
    except FileNotFoundError:
        collection = []
    return collection

if __name__ == '__main__':
    # authenticate with GitHub API
    g = Github(os.environ['GITHUB_TOKEN'])

    # get the repository and issue number from environment variables
    repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])
    issue_number = int(os.environ['INPUT_ISSUE_NUMBER'])

    # get the issue and its body
    issue = repo.get_issue(issue_number)
    body = issue.body

    # parse the body for shoe information
    name_start = body.find('Name:') + 5
    name_end = body.find('\n', name_start)
    name = body[name_start:name_end]

    brand_start = body.find('Brand:') + 6
    brand_end = body.find('\n', brand_start)
    brand = body[brand_start:brand_end]

    size_start = body.find('Size:') + 5
    size_end = body.find('\n', size_start)
    size = body[size_start:size_end]

    # load the current collection
    collection = load_collection()

    # add the new shoe to the collection
    collection = add_shoe(collection, name, brand, size)

    # save the updated collection
    save_collection(collection)
