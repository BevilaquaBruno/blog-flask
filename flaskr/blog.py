from flask import (
  Blueprint, flash, g, redirect, render_template, request, url_for
)
import os
import uuid
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'upload/.')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

@bp.route('/')
def index():
  db = get_db()
  posts = db.execute(
    'SELECT p.id, p.title, p.body, p.created, p.author_id, p.photo, u.username'
    ' FROM post p JOIN user u ON p.author_id = u.id'
    ' ORDER BY p.created DESC'
  ).fetchall()
  data = dict(
    posts= posts,
    img_path= UPLOAD_FOLDER
  )
  return render_template('blog/index.html.jinja', data=data)

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
  if request.method == 'POST':
    title = request.form['title']
    body = request.form['body']
    photo = None
    error = None

    # this needs change, only the name will be gived by filepond
    if 'photo' in request.files:
      photo = request.files['photo']
      if photo is not None and photo.filename != '':
        if allowed_file(photo.filename):
          unique_filename = str(uuid.uuid4())
          photoname = secure_filename(unique_filename)
          photo.save(os.path.join(UPLOAD_FOLDER, photoname))
        else:
          photoname = ''
          error = 'Extension File not allowed'
      else:
        photoname = ''
    else:
      photoname = ''

    if not title:
      error = 'Title is required.'

    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute(
        'INSERT INTO post (title, body, photo, author_id)'
        ' VALUES (?, ?, ?, ?)',
        (title, body, photoname, g.user['id'])
      )
      db.commit()
      return redirect(url_for('blog.index'))
  return render_template('blog/create.html.jinja')

def get_post(id, check_author=True):
  post = get_db().execute(
    'SELECT p.id, p.title, p.body, p.created, p.photo, p.author_id, u.username'
    ' FROM post p JOIN user u ON p.author_id = u.id'
    ' WHERE p.id = ?',
     (id,)
  ).fetchone()

  if post is None:
    abort(404, 'Post id {0} doesn\'t exist.'.format(id))

  if check_author and post['author_id'] != g.user['id']:
    abort(403)

  return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
  post = get_post(id)

  if request.method == 'POST':
    title = request.form['title']
    body = request.form['body']
    photo = None
    error = None

    #this will be changed because of filepond
    if 'photo' in request.files:
      photo = request.files['photo']
      if photo is not None and photo.filename != '':
        if allowed_file(photo.filename):
          photoname = secure_filename(photo.filename)
          photo.save(os.path.join(UPLOAD_FOLDER, photoname))
        else:
          photoname = ''
          error = 'Extension File not allowed'
      else:
        photoname = ''
    else:
      photoname = ''

    if not title:
      error = 'Title is required.'

    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute(
        'UPDATE POST set title = ?, body = ?, photo = ? WHERE id = ?',
        (title, body, photoname, id)
      )
      db.commit()
      return redirect(url_for('blog.index'))

  data = dict(post=post, img_path=UPLOAD_FOLDER)
  return render_template('blog/update.html.jinja', data=data)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
  post = get_post(id)
  db = get_db()
  db.execute('DELETE FROM post WHERE id = ?', (id,))
  db.commit()
  file_path = "%s%s" % (UPLOAD_FOLDER[:-1], post['photo'])
  if(os.path.exists(file_path)):
    os.remove(file_path)

  return redirect(url_for('blog.index'))
