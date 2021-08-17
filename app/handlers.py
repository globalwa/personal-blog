from app import app, db
from flask import render_template, redirect, url_for

@app.errorhandler(401)
def unauthorized(error):
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='Page Not Found'), 200

@app.errorhandler(500)
def unauthorized(error):
    db.session.rollback()
    return render_template('500.html', title='Internal Error'), 200