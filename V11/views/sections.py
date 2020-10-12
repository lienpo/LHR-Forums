from flask import Blueprint, request, session,  render_template

from models.topic import Topic
from models.user import User
from models.section import Section
from models.section import SectionErrors
from models.user import requires_login

section_blueprint = Blueprint('sections', __name__)


@section_blueprint.route('/forums')
def index():
    sections = Section.all()
    users = User.all()
    return render_template('sections/index.html', sections=sections, users=users)


@section_blueprint.route('/new_section', methods=['GET', 'POST'])
@requires_login
def new_section():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        section = Section(title, description, session['username'])
        section.save()

        sections = Section.all()
        creators = User.all()
        return render_template('sections/index.html', sections=sections, users=creators)
    return render_template('sections/new_section.html')


@section_blueprint.route('/view_section/<string:section_title>')
def view_section(section_title):
    section = Section.get_by_title(section_title)
    creator = User.get_by_username(section.creator_name)
    topics = Topic.all_in_section(section.id)
    users = User.all()
    return render_template('sections/view_section.html', section=section, topics=topics, users=users, creator=creator)
