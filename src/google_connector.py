from google_authenticator import GoogleAuth

class Groups(GoogleAuth):
    
    def __init__(self, domain=None):
        self.domain = domain

        api_name = 'admin'
        api_version = 'directory_v1'
        GoogleAuth.__init__(self, api_name, api_version)
        self.service = GoogleAuth.get_service(self).groups()

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
