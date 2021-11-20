from bs4 import BeautifulSoup
import requests
from html5print import HTMLBeautifier
print("\n=================================\n \
Scraping Real discount website started!\n \
=================================")


# This function handles the case when the soup value is none
# It returns "Not Available" as the default value when the value is none
# or the param default_value if the user passes it
def handle_if_none(soup_item=None, default_value=None):
    if soup_item is None:
        if default_value is not None:
            return default_value
        else:
            return "Not available"
    else:
        return soup_item.text


# This function is for preparing the first of the html file
# and adding the opening tags of html and body as well as the first dev tags
def initialize():
    course_content_file = open("courses.html", "w")
    course_content_file.write("<html><body>")
    course_content_file.write(
        "<head>\
        <link rel='stylesheet' type='text/css' href='css/bootstrap.css'>\
        <link rel='stylesheet' type='text/css' href='css/style.css'>\
        </head>")
    course_content_file.write(
        '<div class="container"><div class="row">')
    course_content_file.close()


# This function close the html file and added the closing tags of
#  html and body as well as the first dev tags
def finalize():
    course_content_file = open("courses.html", "a")
    course_content_file.write('</div></div></body></html>')
    course_content_file.close()


# This function is only for beautifying the html file for better readability
def beautifyHTML():
    print("Beautifying the html file")
    with open("courses.html", "r") as f:
        html_content = f.read()
    html_beautified = HTMLBeautifier.beautify(html_content)
    with open("courses.html", "w") as f:
        f.write(html_beautified)


# This is the main function which is called to start the scraping
def scrap(url, pageNext=2, current_page=1):
    curent_page = current_page
    print("Scrapping page {}".format(curent_page))
    page = requests.get(url+"?page="+str(curent_page))
    soup = BeautifulSoup(page.content, 'html.parser')
    courses = soup.find_all(
        'div', class_='col-sm-12 col-md-6 col-lg-4 col-xl-4')
    course_content_file = open("courses.html", "a")
    course_content_file.write("<h1>Page {}</h1>".format(curent_page))
    for course in courses:

        udemy_link = course.find('a', {'href': True})
        if(udemy_link is None):
            pass
        else:
            udemy_link = "https://www.real.discount" + \
                udemy_link.get('href')
            store_name = handle_if_none(
                course.find('span', class_="card-store"))
            card = course.find('div', class_='card')
            img = card.find('img')['src']
            title = card.find('h3', class_="card-title").text
            rating = handle_if_none(soup.find('div', class_="star-rating"))
            category = handle_if_none(card.find('span', class_="card-cat"))
            duration = card.find(
                'div', class_="card-duration")
            duration = handle_if_none(duration.find('div'))
            price = handle_if_none(card.find('span', class_="card-price-sale"))
            page_details = requests.get(udemy_link)

            page_details_soup = BeautifulSoup(
                page_details.content, 'html.parser')
            link_div = page_details_soup.find(
                'div', class_="col-xs-12 col-md-12 col-sm-12 text-center")
            href = link_div.find('a', {'target': '_blank'})
            print("Href:", href)

            if(href is None):
                pass
            else:
                href = href.get('href')
                if(href.__contains__("https://www.udemy.com/")):
                    course_lnk = href.split("https://www.udemy.com/")[1]
                    href = "https://www.udemy.com/" + course_lnk

            udemy_link = href
            html_content = '<div class="col-4 mb-2">\
           <div class="card text-left">\
           <img class="card-img-top" src="{}" alt="">\
           <div class="card-body">\
           <h4 class="card-title">{}</h4>\
           <hr>\
           <p class="card-text"><span class="font-weight-bold">Store</span>:{}</p>\
           <p class="card-text"><span class="font-weight-bold">Rating</span>:{}</p>\
           <p class="card-text"><span class="font-weight-bold">Category</span>:{}</p>\
           <p class="card-text"><span class="font-weight-bold">Price</span>:{}</p>\
           <p class="card-text"><span class="font-weight-bold">Duration</span>:{}</p>\
           </div>\
           <div class="card-footer text-right">\
           <a href="{}" class="btn btn-primary" target="_blank">Go to Course</a>\
           </div>\
           </div></div>'.format(
                img, title, store_name, rating, category, price, duration, udemy_link
            )
            course_content_file.write(html_content)

    if curent_page == pageNext:
        course_content_file.close()
        return

    else:
        course_content_file.close()
        curent_page += 1
        scrap(url, pageNext, curent_page)
