from flask import Blueprint, request, session, url_for, render_template, redirect

topic_blueprint = Blueprint('topics', __name__)


@topic_blueprint.route('/topics')
def index():
    return render_template('topics/index.html')


@topic_blueprint.route('/new_topic')
def new_topic():
    return render_template('topics/new_topic.html')


@topic_blueprint.route('/view_topic.html')
def view_topic():
    return render_template('topics/view_topic.html')
