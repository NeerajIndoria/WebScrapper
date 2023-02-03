from bs4 import BeautifulSoup
import requests
import pandas

URL = []
Name = []
Price = []
Rating = []
Reviews = []

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 "
                  "Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
}
start_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"


def scrape_page(url):
    print("URL: " + url)
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.content, "html.parser")
    get_data(soup)

    next_page_link = soup.find("a",
                               class_="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator")
    if next_page_link is not None:
        print("next")
        link = next_page_link.get("href")
        href = f"https://www.amazon.in{link}"
        scrape_page(href)
    else:
        print("Done")


def get_data(content):
    product_name = content.find_all("span", class_="a-size-medium a-color-base a-text-normal")
    for i in range(len(product_name)):
        Name.append(product_name[i].text)
    product_url = content.find_all("a",
                                   class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
    for i in range(len(product_url)):
        URL.append(product_url[i].get('href'))
    product_price = content.find_all("span", class_="a-price-whole")
    for i in range(len(product_price)):
        Price.append(product_price[i].text)
    product_rating = content.find_all("span", class_="a-icon-alt")
    for i in range(len(product_rating)):
        Rating.append(product_rating[i].text)
    product_reviews = content.find_all("span", class_="a-size-base s-underline-text")
    for i in range(len(product_reviews)):
        Reviews.append(product_reviews[i].text)


def main():
    scrape_page(start_url)
    df = {
        'url': URL[slice(440)],
        'name': Name[slice(440)],
        'price': Price[slice(440)],
        'rating': Rating[slice(440)],
        'reviews': Reviews[slice(440)]
    }

    dataset = pandas.DataFrame(data=df)
    dataset.to_csv("Product_data_part1.csv")


cont = pandas.read_csv("Product_data_part1.csv")
cont = cont['url']


for url in cont:
    ur = f"https://www.amazon.in{url}"
    resp = requests.get(ur, headers=header)
    sp = BeautifulSoup(resp.text, 'html.parser')
    #
    desc = sp.find_all("span", class_="a-list-item")
    for i in range(len(desc)):
        print(desc[i].text)

if __name__ == "__main__":
    main()
