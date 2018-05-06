# bachelor_data
Scraping data from the ABC shows The Bachelor and The Bachelorette.

Just run the script to get the images from the Bachelor Wiki. This is running on the assumption that all the URLs are of the form:

`http://bachelor-nation.wikia.com/wiki/File:{first_name}_({show_name}_{season}).jpg`

or 

`http://bachelor-nation.wikia.com/wiki/File:{first_name}_{last_initial}._({show_name}_{season}).jpg"`

To run, install requests first (`pip install requests`), and then just run the script in the same folder as the CSV files.