# cs1951_final_project

### Style

Checklist before pushing:
- Using single quotes?
- Ran using python3?
- Indent using spaces, not tabs?

Notes on albums.csv:
- I threw out any release_dates that weren't precise to the day. The reasoning behind this was: (1) since we're going to try to predict something specific to dates, it would be almost useless to just have the release year for an album and (2) it was easier.
- I grabbed the 640px by 640px (largest size) url for image_url

Notes on artists.csv:
- I grabbed the 640px by 640px (2nd largest size) url for artist_image_url

Notes on schema:
- image_url in the 'albums' table should be renamed to 'album_image_url' to be consistent with the image url naming convention for the 'artists' table

### Running Node server

If this is your first time, make sure to install all dependencies:

`cd` to the main `/node` directory and run: `npm install`

To run: `node app/server.js`

To view: Go to browser and navigate to: `localhost:<the-port-number>`

### Other Node things

When installing a new package: `npm install <name-of-package> --save`
