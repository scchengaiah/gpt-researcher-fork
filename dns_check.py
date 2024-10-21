import socket
import requests
import argparse

def check_dns(domain):
    try:
        # Try to resolve the domain name to an IP address
        ip = socket.gethostbyname(domain)
        print(f"DNS Resolution Successful: {domain} -> {ip}")
        return True
    except socket.gaierror:
        print(f"DNS Resolution Failed for: {domain}")
        return False

def check_http(domain, url):
    try:
        # Try to make an HTTP request to check network connectivity
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"HTTP Request Successful: {url}")
            return True
        else:
            print(f"HTTP Request Failed with status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"HTTP Request Failed: {e}")
        return False

if __name__ == "__main__":
    # Parse command-line arguments for URL
    parser = argparse.ArgumentParser(description='Check DNS and HTTP connectivity')
    parser.add_argument('url', type=str, help='The URL to check (e.g., http://www.google.com)')
    args = parser.parse_args()

    # Extract domain from the URL
    domain = args.url.split("//")[-1].split("/")[0]

    # Step 1: Check DNS Resolution
    if check_dns(domain):
        # Step 2: If DNS resolution succeeds, check HTTP connectivity
        check_http(domain, args.url)
