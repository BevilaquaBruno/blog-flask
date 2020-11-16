from flask import (
  Blueprint, send_from_directory
)
import os

bp = Blueprint('uploads', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'upload/.')

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
  return send_from_directory(UPLOAD_FOLDER[:-1], filename)