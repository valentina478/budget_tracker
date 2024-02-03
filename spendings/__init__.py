from flask import Blueprint

sp_bp = Blueprint('spendings', __name__)

from app.spendings import routes