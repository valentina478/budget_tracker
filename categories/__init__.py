from flask import Blueprint

categ_bp = Blueprint('categories', __name__)

from app.categories import routes
