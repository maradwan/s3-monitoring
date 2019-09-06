from flask import request, jsonify
from uuid import uuid4
from .models import Raw_data, db, Geoip,raw_data_schema, raw_datas_schema
from api import app
from urllib.parse import quote_plus
import geoip2.database

reader = geoip2.database.Reader('GeoLite2-City.mmdb')

def get_geoip(ip):
    response = reader.city(ip)
    return (response.country.iso_code,response.country.name,response.city.name,response.postal.code,response.location.latitude,response.location.longitude)

# Create a Data
@app.route('/api', methods=['POST'])
def add_data():
        uuid = uuid4()
        eventSource = request.json['eventSource']
        awsRegion = request.json['awsRegion']
        eventTime = request.json['eventTime']
        eventName = request.json['eventName']
        principalId = request.json['principalId']
        sourceIPAddress = request.json['sourceIPAddress']
        bucketname = request.json['bucketname']
        objectkey = request.json['objectkey']
        objectsize = request.json['objectsize']
        etag = request.json['etag']
        versionId = request.json['versionId']
        sequencer = request.json['sequencer']

        new_raw_data = Raw_data(uuid, eventSource, awsRegion, eventTime, eventName, principalId, sourceIPAddress, bucketname, objectkey, objectsize, etag, versionId, sequencer )

        db.session.add(new_raw_data)
        db.session.commit()

        new_geoip = get_geoip(sourceIPAddress)
        geoip = Geoip(new_geoip[0], new_geoip[1], new_geoip[2], new_geoip[3], new_geoip[4], new_geoip[5], uuid)

        db.session.add(geoip)
        db.session.commit()      
 
        return raw_data_schema.jsonify(new_raw_data)

# Update a Data
@app.route('/api/', methods=['PUT'])
def update_data():
  name = request.args.to_dict()
  objectkey = quoting_objects(name)
 
  try:
      data = Raw_data.query.filter_by(objectkey=objectkey , bucketname=name['bucketname'], versionId=name['versionId']).first()
  except:
      return jsonify('Request is not find object '),401

  if data is None:
      return jsonify('Not Found'),404

  try:
      eventSource = request.json['eventSource']
      awsRegion = request.json['awsRegion']
      eventTime = request.json['eventTime']
      eventName = request.json['eventName']
      principalId = request.json['principalId']
      sourceIPAddress = request.json['sourceIPAddress']
      bucketname = request.json['bucketname']
      objectsize = request.json['objectsize']
      etag = request.json['etag']
      sequencer = request.json['sequencer']

      data.eventSource = eventSource
      data.awsRegion = awsRegion
      data.eventTime = eventTime
      data.eventName = eventName
      data.principalId = principalId
      data.sourceIPAddress = sourceIPAddress
      data.bucketname = bucketname
      data.objectsize = objectsize
      data.etag = etag
      data.sequencer = sequencer

      db.session.commit()
      return jsonify(objectkey=objectkey)
  except:
      return jsonify('Misunderstood Request'),400

# rename a Data
@app.route('/api/rename', methods=['PUT'])
def rename_data():
  name = request.args.to_dict()
  objectkey = quoting_objects(name)

  try:
      data = Raw_data.query.filter_by(objectkey=objectkey , bucketname=name['bucketname'], etag=name['etag']).first()
  except:
      return jsonify('Request is not find object '),401

  if data is None:
      return jsonify('Not Found'),404

  try:
      eventSource = request.json['eventSource']
      awsRegion = request.json['awsRegion']
      eventTime = request.json['eventTime']
      eventName = request.json['eventName']
      principalId = request.json['principalId']
      sourceIPAddress = request.json['sourceIPAddress']
      bucketname = request.json['bucketname']
      objectsize = request.json['objectsize']
      etag = request.json['etag']
      versionId = request.json['versionId']
      sequencer = request.json['sequencer']

      data.eventSource = eventSource
      data.awsRegion = awsRegion
      data.eventTime = eventTime
      data.eventName = eventName
      data.principalId = principalId
      data.sourceIPAddress = sourceIPAddress
      data.bucketname = bucketname
      data.objectsize = objectsize
      data.etag = etag
      data.versionId = versionId
      data.sequencer = sequencer

      db.session.commit()
      return jsonify(objectkey=objectkey)

  except:
      return jsonify('Misunderstood Request'),400

# Get Single Data
@app.route('/api/rename/', methods=['GET'])
def get_rename_data():
  name = request.args.to_dict()
  objectkey = quoting_objects(name)
  
  try:
      data = Raw_data.query.filter_by(objectkey=objectkey , bucketname=name['bucketname']).first()
      if data is None:
          return jsonify('Not Found'),404
      return raw_data_schema.jsonify(data)
  except:
      return jsonify('Misunderstood Request'),400

# Get Single Data
@app.route('/api/', methods=['GET'])
def get_data():
  name = request.args.to_dict()
  objectkey = quoting_objects(name)

  try:
      data = Raw_data.query.filter_by(objectkey=objectkey , bucketname=name['bucketname'], versionId=name['versionId']).first()
      if data is None:
          return jsonify('Not Found'),404
      return raw_data_schema.jsonify(data)
  except:
      return jsonify('Misunderstood Request'),400


def quoting_objects(name):
    objectname = []
    for i in name['objectkey'].split('/'):
        objectname.append(quote_plus(i))
    return '/'.join(objectname)
