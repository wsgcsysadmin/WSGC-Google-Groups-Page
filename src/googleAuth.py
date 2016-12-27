from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

settings = {
    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/[app_name].json
    'scopes': (
        'https://www.googleapis.com/auth/admin.directory.group',
        'https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/admin.directory.group.member',),
    'secrets': os.path.join('.', 'client_secret.json'), # aka CLIENT_SECRET_FILE
    'app_name': 'WSGC Google Groups List', # aka APPLICATION_NAME
}

def get_credentials():
    """
        Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
    """
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
    'wsgc-google-groups-list.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(settings['secrets'], settings['scopes'])
        flow.user_agent = settings['app_name']
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)

    return credentials

def get_service(api_name='admin', api_version='directory_v1'):
    """
        Gets the service object for given api

        Returns:
            Service, the obtained Google Service object
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build(api_name, api_version, http=http)

    return service

