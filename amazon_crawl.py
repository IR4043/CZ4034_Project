import requests
from bs4 import BeautifulSoup


def get_soup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2})
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_reviews(soup, review_list, product_asin):
    try:
        reviews = soup.find_all('div', {'data-hook': 'review'})
        for item in reviews:
            size = ""
            color = ""
            service_provider = ""
            product_grade = ""
            review_title = item.find('a', {'data-hook': 'review-title'})
            title = review_title.text.strip()
            rating = float(
                item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip())
            reviewDate = item.find('span', {'data-hook': 'review-date'}).text.strip()
            reviewDescription = item.find('span', {'data-hook': 'review-body'}).text.strip()
            variant = item.find('a', {'data-hook': 'format-strip'})
            if variant:
                text = variant.get_text(separator="|")
                attributes = text.split('|')
                size = attributes[0].split(': ')[1].strip()
                color = attributes[1].split(': ')[1].strip()
                service_provider = attributes[2].split(': ')[1].strip()
                product_grade = attributes[3].split(': ')[1].strip()

            review_link = "https://www.amazon.com/" + review_title.get('href')
            images = item.find_all('img', {'data-hook': 'review-image-tile'})
            image_links = []
            if images:
                for image in images:
                    src = image.get('src')
                    image_links.append(src)

            review = {
                'title': title,
                'rating': rating,
                'productAsin': product_asin,
                'reviewDate': reviewDate,
                'reviewDescription': reviewDescription,
                'size': size,
                'color': color,
                'service_provider': service_provider,
                'product_grade': product_grade,
                'review_link': review_link,
                'image_links': image_links
            }

            review_list.append(review)
    except:
        pass


def scrape(link):
    review_list = []
    split_list = link.split("/")
    productAsin = split_list[5]
    for n in range(1, 2):
        soup = get_soup(link + str(n))
        print(f'Getting Page: {n}')
        get_reviews(soup, review_list, productAsin)
        if not soup.find('li', {'class': 'a-disabled a-last'}):
            pass
        else:
            break
    print("Scraping is Finished")
    return review_list
