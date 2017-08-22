README for RVSVP Tracking App

Last updated 8/22/17

The purpose of this app is to allow people to track RSVPs to (daily) meetings or events.
After registering for the site, a given participant can return to the site and use
his or her phone number to RSVP for the next day's meeting or event.
The administrator of the site has the ability to view all database entrants as well
as stats on how often each participant has attended.  Further, the admin can create
new users in admin mode and can also reset the RSVP count for each day.

This app also contains functionality for sending text messages to participants using
the Twilio API--at this point the text message functionality is limited to informing
RSVP'ed participants of the status of the next day's meeting/event.

This app uses Python, Flask, a SQLAlchemy to query a SQLite database and Jinja2 to 
render the front edge web pages.  In order to run this app on a local machine the 
user should execute the following steps:
1. Create a directory for the folder.
2. Install a virtual environment using pip install virtualenv
3. Install Flask using pip install Flask
4. Navigate to the project directory and type "source scripts/activate" to 
   activate the virtual environment
5. Type python database_setup.py to initialize the database
6. Type python app.py to run the app on localhost:5000

The main files for this program are database_setup.py which creates the Users
database, app.py which contains all of the Python code for performing CRUD operations
on that database as well as handling GET and POST requests from the browser.
The templates folder contains all of the HTML templates that receives information
from the database through Flask and Jinja2.  The static folder contains the css
stylesheets related to the app.

The following paths are available within the app:
1. localhost:5000/ is the homepage where new users can register and existing users
   can RSVP for the next day's meeting/event
2. localhost:5000/admin uses Flask's built in admin functionality and contains a
   button for resetting the count for the next day's meeting as well as a link
   to /admin/user
3. localhost:5000/admin/user contains all of the database data for registered users
   including built in Flask modules for manually adding new users and editing existing
   information
4. localhost:5000/unsubscribe allows registered users to unsubscribe from the app
5. localhost:5000/broadcast makes a call to the Twilio API to send text messages to
   all users who are currently RSVP'ed within the app

In order to stop the local server, type ctrl+C and the deactivate to stop the
virtual environment.

Specific permissions for admin functionality are forthcoming.