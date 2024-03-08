import os
import requests
import gzip
from datetime import datetime

def download_file(url, destination):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return True
    else:
        print(f"Failed to download {url}")
        return False

def is_gzipped(file_path):
    with open(file_path, 'rb') as file:
        return file.read(2) == b'\x1f\x8b'

def unzip_gzip_file(gzip_file_path, output_file_path):
    with gzip.open(gzip_file_path, 'rb') as gz_file:
        with open(output_file_path, 'wb') as new_file:
            for chunk in iter(lambda: gz_file.read(4096), b''):
                new_file.write(chunk)
    os.remove(gzip_file_path)  # Delete the original gzip file

def download_and_process_files(parent_dir, date_str):
    # Convert date string to yyyy/mm/dd format
    date = datetime.strptime(date_str, "%Y/%m/%d").strftime("%Y/%m/%d")

    # URLs for regular TSV files
    urls = [
        f'https://ton.twimg.com/birdwatch-public-data/{date}/notes/notes-00000.tsv',
        f'https://ton.twimg.com/birdwatch-public-data/{date}/noteStatusHistory/noteStatusHistory-00000.tsv',
        f'https://ton.twimg.com/birdwatch-public-data/{date}/userEnrollment/userEnrollment-00000.tsv'
    ]

    # Download regular TSV files
    for url in urls:
        filename = url.split('/')[-1]
        destination = os.path.join(parent_dir, filename)
        download_file(url, destination)

    # Directory for ratings
    ratings_dir = os.path.join(parent_dir, 'ratings')
    os.makedirs(ratings_dir, exist_ok=True)

    # URLs for TSV files (potentially gzipped)
    gz_urls = [
        f'https://ton.twimg.com/birdwatch-public-data/{date}/noteRatings/ratings-00002.tsv',
        f'https://ton.twimg.com/birdwatch-public-data/{date}/noteRatings/ratings-00000.tsv',
        f'https://ton.twimg.com/birdwatch-public-data/{date}/noteRatings/ratings-00003.tsv',
        f'https://ton.twimg.com/birdwatch-public-data/{date}/noteRatings/ratings-00001.tsv',
        f'https://ton.twimg.com/birdwatch-public-data/{date}/noteRatings/ratings-00004.tsv',
        f'https://ton.twimg.com/birdwatch-public-data/{date}/noteRatings/ratings-00005.tsv',
        f'https://ton.twimg.com/birdwatch-public-data/{date}/noteRatings/ratings-00006.tsv',
        f'https://ton.twimg.com/birdwatch-public-data/{date}/noteRatings/ratings-00007.tsv'
    ]

    # Download and process TSV files
    for url in gz_urls:
        filename = url.split('/')[-1]
        destination = os.path.join(ratings_dir, filename)

        if download_file(url, destination):
            if is_gzipped(destination):
                unzip_gzip_file(destination, destination[:-3])  # Remove .gz for output file
            else:
                print(f"{filename} is not gzipped. No unzipping necessary.")

# Usage Example
parent_dir = '.'  # Replace with your parent directory path
date_str = '2024/03/07'  # Replace with your date
download_and_process_files(parent_dir, date_str)
