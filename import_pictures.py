import requests
import csv
from bs4 import BeautifulSoup


def possible_urls(name, show_name, season):
    """
    Returns the possible URLs for a character. 
    """
    split_name = name.split()
    first_name = split_name[0]
    last_initial = name.split()[-1][0]  # May not be correct
    urls = [f"http://bachelor-nation.wikia.com/wiki/File:{first_name}_({show_name}_{season}).jpg"]
    if len(split_name) > 1:
        urls.append(
            f"http://bachelor-nation.wikia.com/wiki/File:{first_name}_{last_initial}._({show_name}_{season}).jpg")
    return urls

def get_images(infile, outfile, show_name):
    with open(infile) as f, open(outfile, "w", newline="") as out:
        dr = csv.DictReader(f)
        dw = csv.DictWriter(out, fieldnames=dr.fieldnames+["image"])
        dw.writeheader()
        for line in dr:
            image_name = None
            name = line["Name"]
            first_name = name.split()[0]
            last_initial = name.split()[-1][0]  # May not be correct
            season = line["Season"]
            correct_response = None

            # Look at each possible URL and see if any of them return a 200
            for url_idx, url in enumerate(possible_urls(name, show_name, season)):
                r = requests.get(url)
                if r.status_code == 200:
                    correct_response = r
                    break
            if correct_response:
                # Let's do the damn thing
                soup = BeautifulSoup(correct_response.text, "lxml")
                for link in soup.find_all('a'):
                    if link.contents and link.contents[0] == "download":
                        image_link = (link['href'])
                        image_req = requests.get(image_link)

                        # If we used the URL with the middle initial, we should save it
                        # with that middle name.
                        if url_idx == 0:
                            image_name = f"{first_name}_{show_name}_{season}.jpg"
                        else:
                            image_name = f"{first_name}_{last_initial}_{show_name}_{season}.jpg"
                        if image_req.status_code == 200:
                            # Download the image
                            with open("images/"+image_name, "wb") as outpicture:
                                outpicture.write(image_req.content)
                        else:  # Not sure why it would go here...
                            print("Check out "+name+url)
                            image_name = None
            line["image"] = image_name or "NA"
            dw.writerow(line)

if __name__ == "__main__":
    get_images("bachelor_females.csv", "bachelor_females_images.csv", "Bachelor")
    get_images("bachelorette_males.csv", "bachelorette_males_images.csv", "Bachelorette")