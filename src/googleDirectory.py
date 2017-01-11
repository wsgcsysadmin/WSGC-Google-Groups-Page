from googleAuth import GoogleAuth
from httplib2 import ServerNotFoundError

import sys

class User(GoogleAuth):
    
    def __init__(self):
        GoogleAuth.__init__(self, 'admin', 'directory_v1')
        self.name_cache = {}

        try:
            self.service = GoogleAuth.get_service(self).users()
        except ServerNotFoundError:
            print("No connection to Google's servers. Try again later...")    
            sys.exit()

    def get_name_from_id(self, user_id):
        """
            Check to see if we already looked up the username. If not, make
            the API call and add it to the cache.
        """
        name = self.name_cache.get(user_id, None)

        if not name:
            response = self.service.get(userKey=user_id).execute()
            name = response['name']['fullName']
            self.name_cache[user_id] = name

        return name

class Members(GoogleAuth):
    
    def __init__(self):
        GoogleAuth.__init__(self, 'admin', 'directory_v1')

        try:
            self.service = GoogleAuth.get_service(self).members()
        except ServerNotFoundError:
            print("No connection to Google's servers. Try again later...")    
            sys.exit()

    def find_owners(self, group_id):
        """
            Returns a list of owners for a group given its group_id
        """
        owners = self.service.list(groupKey=group_id, roles='OWNER').execute()
        results = []
        if owners.get('members', None):
            for member in owners['members']:
                results.append({
                    'id': member['id'],
                    'email': member['email']})

        return results

class Groups(GoogleAuth):
    
    def __init__(self, domain=None):
        self.domain = domain

        GoogleAuth.__init__(self, 'admin', 'directory_v1')

        try:
            self.service = GoogleAuth.get_service(self).groups()
        except ServerNotFoundError:
            print("No connection to Google's servers. Try again later...")    
            sys.exit()

    def api_groups_list(self, page_token=None):
        """
            Initiates the Google Group's list call:
            https://developers.google.com/admin-sdk/directory/v1/reference/groups/list
        """
        num_results = 200
        
        if page_token:
            response = self.service.list(domain=self.domain, maxResults=num_results, pageToken=page_token).execute()
        else:
            response = self.service.list(domain=self.domain, maxResults=num_results).execute()
            
        token = response.get('nextPageToken', None)

        results = []
        for group in response['groups']:
            group_info = {
                'id': group['id'],
                'name': group['name'],
                'email': group['email']}
            results.append(group_info)

        return results, token
        

    def get_domain_groups(self):
        """
            Gets all groups for the given domain
            
            Returns:
                List, generated list of dictionaries with group info
        """
        results = []

        groups, token = self.api_groups_list()
        results += groups

        while token:
            groups, token = self.api_groups_list(token)
            results += groups

        return results
