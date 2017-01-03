import secrets

from google_connector import Groups

if __name__ == '__main__':
    # Gather Google Data
    groups_handler = Groups(secrets.domain)
    groups = groups_handler.get_domain_groups()

    for group in groups:
        print(group['name'])
    
    # Generate an HTML template
    # Run Flask to host page
