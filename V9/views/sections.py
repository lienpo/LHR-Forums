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
        creator = User.get_by_username(session['username'])
        creator_id = creator.id

        try:
            if not Section.start_section(title, description, creator_id):
                sections = Section.all()
                creators = User.all()
                return render_template('sections/index.html', sections=sections, users=creators)
        except SectionErrors as e:
            return e.message
        sections = Section.all()
        creators = User.all()
        return render_template('sections/index.html', sections=sections, users=creators)
    return render_template('sections/new_section.html')


@section_blueprint.route('/view_section/<string:section_title>')
def view_section(section_title):
    section = Section.get_by_title(section_title)
    creator = User.get_by_id(section.user_id)
    topics = Topic.all_in_section(section.id)
    users = User.all()
    return render_template('sections/view_section.html', section=section, topics=topics, users=users, creator=creator)
