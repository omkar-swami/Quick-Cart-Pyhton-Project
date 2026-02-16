from flask import Blueprint, session, redirect, url_for

logout = Blueprint('logout', __name__)

@logout.route("/logout", methods=['GET', 'POST'])
def logout_index():
    session.clear()
    return redirect(url_for('index'))
