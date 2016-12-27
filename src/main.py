
from googleAuth import get_service

import os
import secrets

def get_all_users(service):
    """Returns a list of all users for the WSGC domain
    
    Returns:
        Dictionary, generated with the following keys:
            fullName
            firstName
            lastName
    """
    response = service.users().list(domain=secrets.domain, orderBy='email', maxResults=100).execute()
    token = response.get('nextPageToken', None)

    users = []
    for user in response['users']:
        users.append((user['name']['fullName']))

    while token:
        response = service.users().list(domain=secrets.domain, orderBy='email', maxResults=100, pageToken=token).execute()
        token = response.get('nextPageToken', None)
        for user in response['users']:
            users.append({
                'fullName': user['name']['fullName'],
                'firstName': user['name']['givenName'],
                'lastName': user['name']['familyName']})

    return users

def get_group_owners(service, group_id):
    response = service.members().list(groupKey=group_id, roles='OWNER').execute()
    owners = []
    members = response.get('members', None)
    if members:
        for person in members:
            owners.append(person['email'])

    return owners

def get_groups(service):
    """Gets all groups for the WSGC domain
    
    Returns:
        List, generated list of dictionaries with group info
    """
    groups = []
    num_results = 200

    response = service.groups().list(domain=secrets.domain, maxResults=num_results).execute()
    token = response.get('nextPageToken', None)
    for group in response['groups']:
        group_info = {
            'name': group['name'],
            'email': group['email']}

        owners = get_group_owners(service, group['id'])
        if len(owners) > 0:
            group_info['owners'] = owners

        groups.append(group_info)

    while token:
        response = service.groups().list(domain=secrets.domain, maxResults=num_results, pageToken=token).execute()
        token = response.get('nextPageToken', None)
        for group in response['groups']:
            group_info = {
                'name': group['name'],
                'email': group['email']}
            owners = get_group_owners(service, group['id'])

            if len(owners) > 0:
                group_info['owners'] = owners

            groups.append(group_info)

    return groups
        
def render_group_page():
    # Get a list of all groups in the domain
    service = get_service()
    groups = get_groups(service)    

def main():
    drive_service = get_service('drive', 'v3')
    return drive_service

if __name__ == '__main__':
    main()
