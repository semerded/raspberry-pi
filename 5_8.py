file = open("dataFile.txt", "w")

file.write("regel 1\n")
file.write("regel 2\n")

file.close()

file = open("dataFile.txt", 'a')
file.write("regel 3\n")
file.write('regel 4\n')
file.close()

file = open("dataFile.txt")
inhoud = file.read()
print(inhoud)
file.close()

import requests, io
website = requests.get(r"https://en.wikipedia.org/wiki/9%2F11_conspiracy_theories")
print(website.content)
website = str(website.content)
website = website.replace("\\n", "\n")
website = website.replace("\\t", "\t")
with io.open('website.txt', "w", encoding="utf8") as file:
    file.write(str(website))
