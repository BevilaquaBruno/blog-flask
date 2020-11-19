from flask import (
  Blueprint, send_from_directory, request
)
from werkzeug.utils import secure_filename
import os
import uuid
from flaskr.utils import (allowed_file)

bp = Blueprint('uploads', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'upload/.')
UPLOAD_TEMP_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'upload/temp/.')
JAVASCRIPT_FOLDER = UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets/javascript/.')

@bp.route('/uploads/img/<filename>')
def uploaded_file(filename):
  file_temp = "%s%s" % (UPLOAD_TEMP_FOLDER[:-1], filename)
  if os.path.isfile(file_temp):
    return send_from_directory(UPLOAD_TEMP_FOLDER[:-1], filename)
  return send_from_directory(UPLOAD_FOLDER[:-1], filename)

@bp.route('/uploads/javascript/<jsfile>')
def uploaded_javascript(jsfile):
  return send_from_directory(JAVASCRIPT_FOLDER[:-1], jsfile)

@bp.route('/uploads/work', methods=['POST', 'DELETE'])
def work():
  if request.method == 'POST':
    if 'photo' in request.files:
      photo = request.files['photo']
      if photo is not None and photo.filename != '':
        if allowed_file(photo.filename, 'img'):
          unique_filename = "%s.%s" % (str(uuid.uuid4()).replace('-', '_'), photo.filename.rsplit('.', 1)[1].lower() )
          photoname = secure_filename(unique_filename)
          photo.save(os.path.join(UPLOAD_TEMP_FOLDER, photoname))
          return photoname
        else:
          photoname = ''
      else:
        photoname = ''
    else:
      photoname = ''
  elif request.method == 'DELETE':
    file_path = "%s%s" % (UPLOAD_TEMP_FOLDER[:-1], request.data.decode('utf-8'))
    if(os.path.exists(file_path)):
      os.remove(file_path)
    return 'deleted'