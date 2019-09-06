from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)

# Init db
db = SQLAlchemy()
# Init ma
ma = Marshmallow(app)


class Raw_data(db.Model):
    __tablename__ = 'raw_data'
    uuid = db.Column(db.String(200), primary_key=True)
    eventSource = db.Column(db.String(200))
    awsRegion =  db.Column(db.String(200))
    eventTime = db.Column(db.String(200))
    eventName = db.Column(db.String(200))
    principalId = db.Column(db.String(200))
    sourceIPAddress = db.Column(db.String(200))
    bucketname = db.Column(db.String(200))
    objectkey = db.Column(db.String(200), primary_key=True)
    objectsize = db.Column(db.Float)
    etag = db.Column(db.String(200))
    versionId = db.Column(db.String(200), primary_key=True)
    sequencer =  db.Column(db.String(200))
    created_at = db.Column(db.DateTime, index=True, default=datetime.now,nullable=False)
    geoip = db.relationship('Geoip', backref='raw_data', lazy=True)


    def __init__(self, uuid, eventSource, awsRegion, eventTime, eventName, principalId, sourceIPAddress, bucketname, objectkey, objectsize, etag, versionId, sequencer ):
         self.uuid = uuid
         self.eventSource = eventSource
         self.awsRegion = awsRegion
         self.eventTime = eventTime
         self.eventName = eventName
         self.principalId = principalId
         self.sourceIPAddress = sourceIPAddress
         self.bucketname = bucketname
         self.objectkey = objectkey
         self.objectsize = objectsize
         self.etag = etag
         self.versionId = versionId
         self.sequencer = sequencer


class Geoip(db.Model):
    __tablename__ = 'geoip'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, index=True, default=datetime.now,nullable=False)
    iso_code = db.Column(db.String(4))
    country = db.Column(db.String(64))
    city = db.Column(db.String(64))
    postcode = db.Column(db.String(16))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    raw_data_uuid = db.Column(db.String(200), db.ForeignKey('raw_data.uuid'), nullable=False)

    def __init__(self, iso_code, country, city, postcode, latitude, longitude, raw_data_uuid ):
         self.iso_code = iso_code
         self.country = country
         self.city = city
         self.postcode = postcode
         self.latitude =  latitude
         self.longitude = longitude
         self.raw_data_uuid = raw_data_uuid

# raw_data Schema
class RawdataSchema(ma.Schema):
    class Meta:
        fields = ('uuid', 'eventSource', 'awsRegion', 'eventTime', 'eventName', 'principalId', 'sourceIPAddress', 'bucketname', 'objectkey', 'objectsize', 'etag', 'versionId', 'sequencer' )

# Init schema
raw_data_schema = RawdataSchema(strict=True)
raw_datas_schema = RawdataSchema(many=True, strict=True)
