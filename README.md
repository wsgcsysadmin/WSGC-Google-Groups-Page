# WSGC Google Groups Page
Creates a page to list all google groups within the <a href="https://willystreet.coop">Willystreet Co-op</a>'s Google domain

To get this to work, you'll need to do the following:
  > Obtain client_secret.json and place it in WSGC-Google-Groups-Page/ (or whatever you named the root directory)
  > Create secrets.py and fill it with info. Take a look at main.py to see which bits of info you'll need to supply on your own
  > Create your credentials by running `python main.py [--noauth_local_webserver]

Note: Running the script will open a web browser for you to type your Google credentials. Using `--noauth_local_webserver`
will give you a url to visit on another machine to provide those credentials.
