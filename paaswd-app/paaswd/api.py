import functools
import json 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from paaswd.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['GET'])
def all_users():
    db = get_db()
    query = "SELECT * FROM USER_PASSWD;"
    return json.dumps([tuple(row) for row in db.execute(query).fetchall()])

@bp.route('/users/query', methods=['GET'])
def users_query():
    db = get_db()
    if "name" in request.args.keys():
        name = request.args.get("name")
    else:
        name = "%"

    if "uid" in request.args.keys():
        uid = request.args.get("uid")
    else:
        uid = "%"

    if "gid" in request.args.keys():
        gid = request.args.get("gid")
    else:
        gid = "%"

    if "comment" in request.args.keys():
        comment = request.args.get("comment")
    else:
        comment = "%"

    if "home" in request.args.keys():
        home = request.args.get("home")
    else:
        home = "%"

    if "shell" in request.args.keys():
        shell = request.args.get("shell")
    else:
        shell = "%"
    args = [name, uid, gid, comment, home, shell]
    print(args)
    query = "SELECT * FROM USER_PASSWD WHERE USERNAME LIKE ? AND UID LIKE ? \
            AND GID LIKE ? AND INFO LIKE ? AND HOME_DIR LIKE ? AND SHELL LIKE ?;"
    return json.dumps([tuple(row) for row in db.execute(query,args).fetchall()])        

@bp.route('/users/<int:user_id>', methods=['GET'])
def user_from_uid(user_id):
    db = get_db()
    query = "SELECT * FROM USER_PASSWD WHERE UID=?;"
    return json.dumps([tuple(row) for row in db.execute(query,[str(user_id)]).fetchall()])

@bp.route('/users/<int:user_id>/groups', methods=['GET'])
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
    db = get_db()
    if "name" in request.args.keys():
        name = request.args.get("name")
    else:
        name = "%"

    if "gid" in request.args.keys():
        gid = request.args.get("gid")
    else:
        gid = "%"
    #Okay, so this logic sucks, but I didn't have a way to easily get the intersection of the
    #groups list passed in and the groups list in the column. Not sure if sqlite supports a
    #more robust solution.
    add_string = []
    if "member" in request.args.keys():
        for _ in request.args.getlist("member"):
            add_string.append("GROUP_LIST LIKE ?")
    else:
        member = "%"
    query_groups = "SELECT * FROM USER_GROUP WHERE GROUP_NAME LIKE ? AND GID LIKE ? AND GROUP_LIST LIKE ?;"
    if(len(add_string)>1):
        query_groups = "SELECT * FROM USER_GROUP WHERE GROUP_NAME LIKE ? AND GID LIKE ? AND (" 
        for i in range(len(add_string)-1):
            query_groups += add_string[1] + " AND "
        query_groups += add_string[len(add_string)-1] + ");"
        print(query_groups)
        members = []
        for i in request.args.getlist("member"):
            members.append("%" + i + "%")
        args = [name,gid,*members]
    elif(len(add_string)==1):
        member = "%" + request.args.get("member") + "%"
        args = [name,gid,member]
    else:
        args = [name,gid,member]
    print(args)
    return json.dumps([tuple(row) for row in db.execute(query_groups,args).fetchall()])
    return "test"

@bp.route('/groups/<int:group_id>', methods=['GET'])
def groups_from_gid(group_id):
    db = get_db()
    query = 'SELECT * FROM USER_GROUP WHERE GID = ?;'
    return json.dumps([tuple(row) for row in db.execute(query,[group_id]).fetchall()])