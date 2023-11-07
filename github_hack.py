import os
import requests
import zipfile
import re
from tqdm import tqdm

# GitHub API endpoint for searching repositories
search_url = "https://api.github.com/search/repositories"

# Your GitHub username and personal access token
github_username = "xiaoshun007"
github_token = "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"

# Search query (modify as needed)
search_query = "蓝桥杯"

# Define headers for the API request
headers = {
    "Authorization": f"token {github_token}"
}

# List of repositories to skip (format: owner/repo)
repositories_to_skip = ["personqianduixue/Math_Model"]

# Function to process file name (truncate to 64 characters, replace emojis with '#')
def process_filename(filename):
    # Truncate to 64 characters
    filename = filename[:64]
    return filename

# Send a GET request to the GitHub API to search for repositories
response = requests.get(search_url, headers=headers, params={"q": search_query})

if response.status_code == 200:
    data = response.json()
    # Loop through the search results and process the repositories
    for item in data["items"]:
        repo_name = item["name"]
        repo_owner = item["owner"]["login"]
        repo_url = item["html_url"]

        try:
            if f"{repo_owner}/{repo_name}" in repositories_to_skip:
                print(f"Skipping {repo_owner}/{repo_name}")
                continue

            # Fetch the repository details
            details_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
            details_response = requests.get(details_url, headers=headers)
            if details_response.status_code == 200:
                details = details_response.json()
                about = details.get("description") or repo_name  # Use About or repo name
                about = about.replace('/', '_')
                print(about)

                # Create a directory for the repository
                repo_dir = f"{repo_owner}_{repo_name}"
                os.makedirs(repo_dir, exist_ok=True)

                # Download the repository as a zip file with progress bar
                zip_url = f"{repo_url}/archive/master.zip"
                zip_file_name = process_filename(f"{about}.zip")
                with requests.get(zip_url, stream=True) as zip_response:
                    zip_response.raise_for_status()
                    total_size = int(zip_response.headers.get("content-length", 0))
                    with open(zip_file_name, "wb") as zip_file, tqdm(
                        unit="B", unit_scale=True, unit_divisor=1024, total=total_size
                    ) as progress_bar:
                        for data in zip_response.iter_content(chunk_size=1024):
                            zip_file.write(data)
                            progress_bar.update(len(data))

                # Create an empty txt file and add it to the zip archive
                empty_file_data = b""  # Empty content for the txt file
                with zipfile.ZipFile(zip_file_name, 'a') as zipf:
                    zipf.writestr("empty_file.txt", empty_file_data)

                print(f"Downloaded {repo_name} as {zip_file_name}")
            else:
                print(f"Failed to fetch details for {repo_name}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred for {repo_name}: {e}")
            continue
else:
    print("Failed to search for repositories")

# Clean up: You can remove the extracted repository directories if needed
# Be cautious when removing files and directories in your code
