import urllib.parse
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='URL Encoder')
    parser.add_argument('url', type=str, help='URL to encode')
    args = parser.parse_args()
    print(urllib.parse.quote(args.url, safe='')) 