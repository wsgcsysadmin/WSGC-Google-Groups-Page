
from datetime import datetime
from googleDirectory import Groups, Members, User
from googleapiclient.errors import HttpError
from jinja2 import Environment, FileSystemLoader, select_autoescape

import os

###################################################
## IMPORTANT: You'll need to create your own secrets file with the
## following information:
## 
## domain = 'your_domain'
###################################################
import secrets

SOURCE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(SOURCE_DIR, '../assets')

def gather_group_data():
    print("Pulling data from Google: <", end="", flush=True)
    groups_handler = Groups(secrets.domain)
    member_handler = Members()
    user_handler = User()

    groups = groups_handler.get_domain_groups()
    for group in groups:
        print('.', end="", flush=True)
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
        elif group.get('aliases', None):
            aliases = group['aliases']
            for alias in aliases:
                group['owners'].append({
                    'name': alias,
                    'email': ''})
    print('>')

    return groups

def generate_html_from_groups(groups):
    # Build up the html content
    print("Generating HTML content...")

    html = "{% extends 'base.html' %}"

    html += "{% block date_stamp %}"
    html += "File generated on: "
    html += datetime.today().strftime("%b %d, %Y at %I:%M %p")
    html += "{% endblock date_stamp %}"

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
        if owners:
            for member in owners:
                row_data += "<p>"
                name = member['name']
                email = member['email']
                row_data += '<a href=mailto:"' + email + '">'
                if name:
                    row_data += name
                else:
                    row_data += email
                row_data += '</a>'
                row_data += "</p>"
        else:
            row_data += "<p>"
            row_data += "No owners"
            row_data += "</p>"
        row_data += '</td>'

        row_data += "</tr>"

        html += row_data
        html += "\n"

    html += "{% endblock content_block %}"

    # Use the html content to generate index.html from a template
    env = Environment(
        loader = FileSystemLoader(ASSETS_DIR),
        autoescape = select_autoescape(['html', 'xml'])
    )

    index_contents = env.from_string(html)
    index_filepath = os.path.join(ASSETS_DIR, 'index.html')
    with open(index_filepath, 'w') as index_file:
        index_file.write(index_contents.render())

def build_index_page():
    """
        Generates an index.html file and dumps it in the assets directory
    """
    groups = gather_group_data()
    generate_html_from_groups(groups)
    print("success", end="", flush=True) # passing a message to the deploy script

if __name__ == '__main__':
    build_index_page()
