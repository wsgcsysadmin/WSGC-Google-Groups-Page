import secrets # You'll need to create your own secrets file

from googleDirectory import Groups, Members, User
from googleapiclient.errors import HttpError

if __name__ == '__main__':
    # Gather Google Data
    groups_handler = Groups(secrets.domain)
    member_handler = Members()
    user_handler = User()

    groups = groups_handler.get_domain_groups()
    for group in groups:
        owners = member_handler.find_owners(group['id'])
        group['owners'] = []
        if owners:
            for member in owners:
                try:
                    member_name = user_handler.get_name_from_id(member['id'])
                except HttpError:
                    member_name = None
                group['owners'].append({
                    'name': member_name,
                    'email': member['email']})

    # Generate an HTML template
    # Run Flask to host page

