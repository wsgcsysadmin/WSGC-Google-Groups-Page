import secrets # You'll need to create your own secrets file

from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from googleDirectory import Groups, Members, User
from googleapiclient.errors import HttpError

def gather_group_data():
    print("Pullig data from Google: <", end="", flush=True)
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
    print('>')

    return groups

def generate_html_from_groups(groups):
    # First, build up the html content
    print("Generating HTML content...")

    html = "{% extends 'base.html' %}"

    html += "{% block date_stamp %}"
    html += "File generated on: " + datetime.today().__str__()
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
                row_data += '<a href="' + email + '">'
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

    html += "{% endblock content_block %}"

    # Next, use the html content to generate index.html from a template
    env = Environment(
        loader = FileSystemLoader('../assets'),
        autoescape = select_autoescape(['html', 'xml'])
    )

    index_contents = env.from_string(html)
    with open('../assets/index.html', 'w') as index_file:
        index_file.write(index_contents.render())

def build_index_page():
    groups = gather_group_data()
    generate_html_from_groups(groups)

if __name__ == '__main__':
    build_index_page()
