import functools
import json 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from paaswd.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/register', methods=['GET'])
def register():
    return "register"

@bp.route('/users', methods=['GET'])
def all_users():
    db = get_db()
    query = "SELECT * FROM USER_PASSWD;"
    return json.dumps([tuple(row) for row in db.execute(query).fetchall()])

@bp.route('/users/query', methods=['GET'])
def users_query():
    return "register"

@bp.route('/users/<int:user_id>', methods=['GET'])
def user_from_uid(user_id):
    db = get_db()
    query = "SELECT * FROM USER_PASSWD WHERE UID=?;"
    return json.dumps([tuple(row) for row in db.execute(query,[str(user_id)]).fetchall()])

@bp.route('/users/<user_id>/groups', methods=['GET'])
def user_group_membership(user_id):
    db = get_db()
    subquery = "SELECT USERNAME FROM USER_PASSWD WHERE UID = ?;"
    user_name = str(*tuple(db.execute(subquery,[str(user_id)]).fetchone()))
    query = 'SELECT GROUP_NAME FROM USER_GROUP WHERE GROUP_LIST LIKE ?;'
    return json.dumps([tuple(row) for row in db.execute(query,[user_name]).fetchall()])

@bp.route('/groups', methods=['GET'])
def all_groups():
    db = get_db()
    query = 'SELECT * FROM USER_GROUP;'
    return json.dumps([tuple(row) for row in db.execute(query).fetchall()])

@bp.route('/groups/query', methods=['GET'])
def groups_query():
    return "register"

@bp.route('/groups/<int:group_id>', methods=['GET'])
def groups_from_gid(group_id):
    db = get_db()
    query = 'SELECT * FROM USER_GROUP WHERE GID = ?;'
    return json.dumps([tuple(row) for row in db.execute(query,[group_id]).fetchall()])