#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import *
from models import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from sqlalchemy.sql import func
from flask import g

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

#----------------------------------------------------------------------------#
# Blueprints.
#----------------------------------------------------------------------------#

# from __ import __
# app.register_blueprint(__)

#----------------------------------------------------------------------------#
# Flask_Admin.
#----------------------------------------------------------------------------#

panel = Admin(
    app,
    name='Admin Control Panel',
    template_mode='bootstrap3',
)
panel.add_link(MenuLink(name='Logout', category='', url='/logout'))
panel.add_view(DefaultModelView(User, db.session, column_searchable_list=['username', 'email']))

#----------------------------------------------------------------------------#
# Login.
#----------------------------------------------------------------------------#

login_manager = LoginManager()
login_manager.init_app(app)

class LoginUser(UserMixin):
    @property
    def is_admin(self):
        return self.is_authenticated and self.id == 'admin' 
        # TODO: YOU NEED TO IMPLEMENT THIS!! A SUGGESTION IS ADDING A "ROLE" COLUMN TO THE USER DATABSE


@login_manager.user_loader
def user_loader(username):
    if User.query.filter_by(username=username).first() is None:
        return
    user = LoginUser()
    user.id = username
    return user

#----------------------------------------------------------------------------#
# Controllers.
#    I suggest you create Blueprints for your routes to keep them tidy (up there),
#    but I won't to that here.
#----------------------------------------------------------------------------#

# Set a global variable 'current' before each request
@app.before_request
def before_request():
    if 'current' not in session:
        session['current'] = 'A'  # Default value
    g.current = session['current']

@app.route('/toggle_user')
def toggle_user():
    if session['current'] == 'A':
        session['current'] = 'B'
    else:
        session['current'] = 'A'
    return redirect(request.referrer or url_for('home'))

@app.route('/')
def home():
    random_question = UserSecurityQuestions.query.order_by(func.random()).first()
    existing_follow_request = FollowRequest.query.filter_by(followerusername=g.current).first()
    disable_follow_button = existing_follow_request is not None
    opposite_user = 'B' if g.current == 'A' else 'A'
    return render_template('pages/placeholder.home.html', question=random_question, disable_follow_button=disable_follow_button, opposite_user=opposite_user)

from flask import request

@app.route('/submit_follow_request', methods=['POST'])
def submit_follow_request():
    username = request.form.get('username')
    followerusername = request.form.get('followerusername')
    question = request.form.get('question')
    answer = request.form.get('answer')

    # Create a new FollowReqest instance and save to the database
    new_request = FollowRequest(username='B' if g.current == 'A' else 'A', followerusername=g.current, question=question, answer=answer)
    db.session.add(new_request)
    db.session.commit()

    return redirect(url_for('home'))  # Redirect to the home page or any other page as needed


@app.route('/notification')
def notification():
    follow_requests = FollowRequest.query.filter_by(username=g.current).all()
    return render_template('pages/placeholder.notification.html', follow_requests=follow_requests)

@app.route('/accept_request/<followerusername>', methods=['POST'])
def accept_request(followerusername):
    follow_request = FollowRequest.query.filter_by(username=g.current, followerusername=followerusername).first()
    if follow_request:
        db.session.delete(follow_request)
        db.session.commit()
        flash('Follow request accepted.', 'success')
    return redirect(url_for('notification'))

@app.route('/deny_request/<followerusername>', methods=['POST'])
def deny_request(followerusername):
    follow_request = FollowRequest.query.filter_by(username=g.current, followerusername=followerusername).first()
    if follow_request:
        db.session.delete(follow_request)
        db.session.commit()
        flash('Follow request denied.', 'danger')
    return redirect(url_for('notification'))

@app.route('/profile')
@login_required
def profile():
    if current_user.is_admin:
        return """
            Hello, {}
            <br>
            <a href="/admin/">Admin Panel?</a>
            <a href="/logout">Logout</a>
        """.format(current_user.id)
    return """
        Hello, {}
        <br>
        <a href="/logout">Logout</a>
    """.format(current_user.id)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingsForm(request.form)
    if request.method == 'POST' and form.validate():
        # Handle form submission
        existing_questions = UserSecurityQuestions.query.filter_by(username="A").all()
        existing_question_ids = {q.questionid for q in existing_questions}
        submitted_question_ids = set()

        for i, question_form in enumerate(form.questions):
            question_id = i + 1
            submitted_question_ids.add(question_id)
            question = UserSecurityQuestions.query.filter_by(username="A", questionid=question_id).first()
            if question:
                # Update existing question
                if question.question != question_form.question.data:
                    print(f"Updating question {question_id}: {question.question} -> {question_form.question.data}")
                    question.question = question_form.question.data
            else:
                # Add new question
                new_question = UserSecurityQuestions(username="A", questionid=question_id, question=question_form.question.data)
                db.session.add(new_question)

        # Remove questions that were not submitted
        questions_to_remove = existing_question_ids - submitted_question_ids
        for question_id in questions_to_remove:
            question = UserSecurityQuestions.query.filter_by(username="A", questionid=question_id).first()
            if question:
                db.session.delete(question)

        db.session.commit()
        flash('Settings saved successfully!', 'success')
        return redirect(url_for('settings'))
    else:
        # Populate form with existing questions
        questions = UserSecurityQuestions.query.filter_by(username="A").all()
        question_count = len(questions)
        for i, question in enumerate(questions):
            if i < len(form.questions):
                form.questions[i].question.data = question.question
            else:
                form.questions.append_entry({'question': question.question})
        # Ensure the form has the correct number of fields
        while len(form.questions) < len(questions):
            form.questions.append_entry()
    return render_template('forms/settings.html', form=form)


# Error handlers ------------------------------------------------------------#

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':

    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
