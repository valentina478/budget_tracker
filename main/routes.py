from flask import render_template

from app.main import bp


@bp.route('/')
def get_index():
    return render_template('main/main_page.html')
