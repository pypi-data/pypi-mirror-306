# spotless
Spotless is a spotify management tool to help you remove duplicate tracks from your Spotify library.
https://pypi.org/project/spotless-manager/0.1.1/

Prerequisites:
python needs to be installed
pip if not installed (python get-pip.py)

How to install:
pip install spotless-manager

How to run:
After installing spotless you can simply run 'spotless-manager' in your terminal
You will be sent to login with spotify, and then to take the session id and enter into the terminal
Then you will be prompted to enter a command:
duplicate: will list all of your duplicates

How it works:
The duplicate command matches on track name and all of the artist names. If you have multiple of the same track name that have all of the same artists, those will be marked as duplicates

Behind the scenes:
There is a flask app that is handling all of the routes to authenticate, find duplicates, and delete duplicates. This is hosted on Google Cloud Run. The pip program calls these hosted endpoints so that each user doesn't need a spotify developer account in order to run the program.

Considerations: If you have a large spotify library, this program may take 2-3 minutes to run, this is because of the rate limiting that happens on the spotify api side. Given more time I would use threads and parallelize these calls to improve performance. 