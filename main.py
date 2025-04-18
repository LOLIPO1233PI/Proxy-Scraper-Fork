import time
import concurrent.futures
import requests


# This is a bare version of the original code
# https://github.com/berkay-digital/Proxy-Scraper
# The original code is licensed under the MIT License
#
class ProxyScraper:
    def __init__(self, proxy_list: list[str]):
        self.proxy_list = set(proxy_list)
        self.working_proxies: list[str] = []

    def is_bad_proxy(self, pip):
        try:
            _ = requests.get(
                "http://api.ipify.org/",
                proxies={"http": f"http://{pip}", "https": f"https://{pip}"},
                timeout=5,
            )
            _.raise_for_status()
        except requests.HTTPError:
            print(f"HTTP Error: {pip}")
            return True
        return False

    def check_proxy(self, proxy):
        if self.is_bad_proxy(proxy):
            print(f"Bad proxy: {proxy}")
            return
        self.working_proxies.append(proxy)

    def out_proxies(self, output_file: str = "proxies.txt"):
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.check_proxy, self.proxy_list)
        end_time = time.time()
        print(">> Time taken: ", end_time - start_time, "seconds")
        try:
            with open(output_file, "a") as f:
                f.write("\n".join(self.working_proxies))
            print(f"Working proxies saved to {output_file}")
        except (IOError, OSError) as e:
            print(f"Error writing to file: {e}")

    def update_proxies(self, url: str):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            self.proxy_list = response.text.splitlines()
            print("Proxies updated successfully.")
        except requests.HTTPError as e:
            print(f"Error updating proxies: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


