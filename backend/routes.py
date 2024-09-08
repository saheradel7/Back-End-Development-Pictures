from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data),200


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    pic = None
    for i in data:
        if i["id"] == id:
            pic = i 
    if pic is None: 
        return jsonify({"error":"not found"}),404
    return jsonify(pic),200

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    pic_ids = []
    for i in data:
        pic_ids.append(i["id"])
    
    res = request.get_json()
    if res["id"] in pic_ids:
        return jsonify({"Message": f"picture with id {res['id']} already present"}),302
    
    data.append(res)
    return jsonify({"Message": "Picture created successfully", "id": res["id"]}), 201

    
    
######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pic_ids =[i['id'] for i in data] 
    if id not in pic_ids:
        return jsonify({"message": "picture not found"}),404
    d= request.get_json()
    for i in data:
        if i['id'] == id:
            i["pic_url"] = d["pic_url"]
            i["event_country"] = d["event_country"]
            i["event_state"] = d["event_state"]
            i["event_city"] = d["event_city"]
            i["event_date"] = d["event_date"]
            break
    return jsonify(i),200

######################################################################
# DELETE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data
    pic_ids = [i["id"] for i in data]
    if id not in pic_ids:
        return jsonify({"message": "picture not found"}), 404
    data = [d for d in data if d['id'] != id]
    return jsonify({"message": "deleted"}),204