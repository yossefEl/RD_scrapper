
import scrapper
import webbrowser
import os
import sys

languages_url = "https://www.real.discount/subcategory/language/"
main_url = "https://www.real.discount/free-courses/"

# Prepare the html file
scrapper.initialize()

# Handling arguments
pageStart = 10
if len(sys.argv) == 3:
    main_url = sys.argv[1]
    pageStart = int(sys.argv[2])
else:
    pageStart = sys.argv[1]


# Get the list of courses
scrapper.scrap(main_url, pageNext=int(pageStart))

# Close the html file
scrapper.finalize()

# Beautify html file
scrapper.beautifyHTML()

# Open file on chrome
webbrowser.open('file://' + os.path.realpath("courses.html"))
