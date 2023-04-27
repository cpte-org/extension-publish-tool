import argparse
import os
import requests
import subprocess
from dotenv import load_dotenv

load_dotenv()

def publish_chrome(extension_id, client_id, client_secret, refresh_token, zip_file_path):
    # Get access token
    url = 'https://accounts.google.com/o/oauth2/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    response = requests.post(url, data=data)
    access_token = response.json()['access_token']

    # Upload the extension
    upload_url = f'https://www.googleapis.com/upload/chromewebstore/v1.1/items/{extension_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'x-goog-api-version': '2'
    }
    with open(zip_file_path, 'rb') as file:
        response = requests.put(upload_url, headers=headers, data=file)

    # Publish the extension
    publish_url = f'https://www.googleapis.com/chromewebstore/v1.1/items/{extension_id}/publish'
    response = requests.post(publish_url, headers=headers)

    print("Chrome Web Store:", response.json())

def publish_firefox(api_key, api_secret, xpi_file_path, extension_version, extension_id, download_dir):
    cmd = f'sign-addon --api-key "{api_key}" --api-secret "{api_secret}" --xpi "{xpi_file_path}" --version "{extension_version}" --channel "listed" --id "{extension_id}" --download-dir "{download_dir}"'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        print("Firefox Add-ons: Successfully signed and published")
    else:
        print("Firefox Add-ons:", stderr.decode())

def publish_edge(extension_id, tenant_id, client_id, client_secret, refresh_token, zip_file_path):
    # Get access token
    url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'resource': 'https://manage.devcenter.microsoft.com'
    }
    response = requests.post(url, data=data)
    access_token = response.json()['access_token']

    # Upload the extension
    upload_url = f'https://manage.devcenter.microsoft.com/v1.0/my/extensions/{extension_id}/package'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/zip'
    }
    with open(zip_file_path, 'rb') as file:
        response = requests.put(upload_url, headers=headers, data=file)

    print("Microsoft Edge Add-ons:", response.json())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto-publish browser extension to Chrome, Firefox, and Edge stores.")
    
    parser.add_argument("--chrome", action="store_true", help="Publish to Chrome Web Store")
    parser.add_argument("--firefox", action="store_true", help="Publish to Firefox Add-ons")
    parser.add_argument("--edge", action="store_true", help="Publish to Microsoft Edge Add-ons")

    parser.add_argument("--extension_id", required=True, help="Extension ID")
    parser.add_argument("--zip_file_path", required=True, help="Path to the extension ZIP file")

    args = parser.parse_args()

    if args.chrome:
        publish_chrome(args.extension_id, os.getenv("CHROME_CLIENT_ID"), os.getenv("CHROME_CLIENT_SECRET"), os.getenv("CHROME_REFRESH_TOKEN"), args.zip_file_path)

    if args.firefox:
        publish_firefox(os.getenv("FIREFOX_API_KEY"), os.getenv("FIREFOX_API_SECRET"), args.zip_file_path.replace(".zip", ".xpi"), "your_extension_version", args.extension_id, "path/to/download/signed/xpi")

    if args.edge:
        publish_edge(args.extension_id, os.getenv("EDGE_TENANT_ID"), os.getenv("CHROME_CLIENT_ID"), os.getenv("CHROME_CLIENT_SECRET"), os.getenv("CHROME_REFRESH_TOKEN"), args.zip_file_path)
