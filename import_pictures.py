import requests
import csv
from bs4 import BeautifulSoup


def get_images(infile, outfile, show_name):
    with open(infile) as f, open(outfile, "w", newline="") as out:
        dr = csv.DictReader(f)
        dw = csv.DictWriter(out, fieldnames=dr.fieldnames+["image"])
        dw.writeheader()
        for line in dr:
            image_name = None
            name = line["Name"]
            first_name = name.split()[0]
            season = line["Season"]
            url = f"http://bachelor-nation.wikia.com/wiki/File:{first_name}_({show_name}_{season}).jpg"
            r = requests.get(url)
            if r.status_code == 200:
                # Let's do the damn thing
                soup = BeautifulSoup(r.text, "lxml")
                for link in soup.find_all('a'):
                    if link.contents and link.contents[0] == "download":
                        image_link = (link['href'])
                        image_req = requests.get(image_link)
                        image_name = f"{first_name}_{show_name}_{season}.jpg"
                        if image_req.status_code == 200:
                            # Download the image
                            with open("images/"+image_name, "wb") as outpicture:
                                outpicture.write(image_req.content)
                        else:  # Not sure why it would go here...
                            image_name = None
            line["image"] = image_name or "NA"
            dw.writerow(line)

if __name__ == "__main__":
    get_images("bachelor_females.csv", "bachelor_females_images.csv", "Bachelor")
    get_images("bachelorette_males.csv", "bachelorette_males_images.csv", "Bachelorette")