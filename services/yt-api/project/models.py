from project import db
from flask_sqlalchemy import SQLAlchemy

class Video(db.Model):
    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(128), unique=True, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    thumbnail = db.Column(db.String(512), nullable=False)
    channel_title = db.Column(db.String(128), nullable=False)
    publish_time = db.Column(db.DateTime(timezone=True), nullable=False)


    def __init__(self, video_id, title, description, thumbnail, channel_title, publish_time):
        self.video_id = video_id
        self.title = title
        self.description = description
        self.thumbnail = thumbnail
        self.channel_title = channel_title
        self.publish_time = publish_time