from flask import (
  Blueprint, send_from_directory
)
import os

bp = Blueprint('uploads', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'upload/.')
UPLOAD_TEMP_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'upload/temp/.')
JAVASCRIPT_FOLDER = UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets/javascript/.')

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
  file_temp = "%s%s" % (UPLOAD_TEMP_FOLDER[:-1], filename)
  if os.path.isfile(file_temp):
    return send_from_directory(UPLOAD_TEMP_FOLDER[:-1], filename)
  return send_from_directory(UPLOAD_FOLDER[:-1], filename)

@bp.route('/uploads/javascript/<filename>')
def uploaded_javascript(filename):
  return send_from_directory(JAVASCRIPT_FOLDER[:-1], filename)