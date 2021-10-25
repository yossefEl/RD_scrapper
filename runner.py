
import scrapper
import webbrowser
import os
import sys

languages_url = "https://www.real.discount/subcategory/language/"
main_url = "https://www.real.discount/free-courses/"

scrapper.initialize()

pageStart = 10
if len(sys.argv) == 3:
    main_url = sys.argv[1]
    pageStart = int(sys.argv[2])
else:
    pageStart = sys.argv[1]
scrapper.scrap(main_url, pageNext=int(pageStart))

webbrowser.open('file://' + os.path.realpath("courses.html"))
