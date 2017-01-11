import secrets # You'll need to create your own secrets file

from jinja2 import Environment, FileSystemLoader, select_autoescape
from googleDirectory import Groups, Members, User
from googleapiclient.errors import HttpError

if __name__ == '__main__':
    # Gather Google Data
    print("Scraping data from Google...")
    groups_handler = Groups(secrets.domain)
    member_handler = Members()
    user_handler = User()

    groups = groups_handler.get_domain_groups()
    for group in groups:
        print('\tProcessing: ' + group['name'])
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
    print("Generating HTML content...")
    html = "{% extends 'base.html' %}"
    html += "{% block content_block %}"
    for group in groups:
        row_data = "<tr>"

        row_data += '<td class="name">'
        row_data += group['name']
        row_data += '</td>'

        row_data += '<td class="email">'
        row_data += '<a href=mailto:"' + group['email'] + '">'
        row_data += group['email']
        row_data += '</a>'
        row_data += '</td>'

        row_data += '<td class="owners">'
        owners = group['owners']
        row_data += "<ul>"
        if owners:
            for member in owners:
                row_data += "<li>"
                name = member['name']
                email = member['email']
                row_data += '<a href="' + email + '">'
                if name:
                    row_data += name
                else:
                    row_data += email
                row_data += '</a>'
                row_data += "</li>"
        else:
            row_data += "<li>"
            row_data += "No owners"
            row_data += "</li>"
        row_data += "</ul>"
        row_data += '</td>'

        row_data += "</tr>"
        html += row_data

    html += "{% endblock content_block %}"

    env = Environment(
        loader = FileSystemLoader('../assets'),
        autoescape = select_autoescape(['html', 'xml'])
    )

    index_contents = env.from_string(html)
    with open('../assets/index.html', 'w') as index_file:
        index_file.write(index_contents.render())


    # Run Flask to host page
