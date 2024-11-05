import sys
import os
from intelliw.utils.storage_service import StorageService


def download(url, path):
    downloader = StorageService(url, "download")
    downloader.download(path)
    return


if __name__ == '__main__':
    file_url = sys.argv[1]
    save_path = sys.argv[2]
    download(file_url, save_path)
