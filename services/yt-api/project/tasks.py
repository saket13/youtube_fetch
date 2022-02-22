import json
import requests
import dateutil
from datetime import datetime
from project.models import Video
from project import app, db, celery_app

@celery_app.task
def fetch():
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    
    search_params = {
        'part' : 'snippet',
        'q' : 'cricket',
        'maxResults' : 10,
        'type' : 'video'
    }

    try:
        latest_entity = Video.query.order_by(Video.publish_time.desc()).limit(1).all()
        latest_publish_time = app.config['DEFAULT_PUBLISH_TIME']
        if len(latest_entity):
            latest_publish_time = latest_entity[0].publish_time
            latest_publish_time = datetime.strptime(str(latest_publish_time), '%Y.%m.%dT%H:%M:%S+00:00Z')
            search_params.update({'publishedAfter' : latest_publish_time})
        
        search_params.update({'publishedAfter' : latest_publish_time,
                               'key' : app.config['YOUTUBE_DATA_API_KEY']}) 

        r = requests.get(search_url, params=search_params)
        results = r.json()['items']
        

        for item in results:
            video_id = item.get('id').get('videoId')
            video_title = item.get('snippet').get('title')
            video_desc = item.get('snippet').get('description')
            video_thumbnail = item.get('snippet').get('thumbnails').get('default').get('url')
            channel_title = item.get('snippet').get('channelTitle')
            video_publish_time_iso = item.get('snippet').get('publishTime')
            video_publish_time = datetime.fromisoformat(video_publish_time_iso[:-1] + '+00:00')
            
            db.session.add(Video(video_id=video_id, 
                                 title=video_title, 
                                 description=video_desc, 
                                 thumbnail=video_thumbnail,
                                 channel_title=channel_title,
                                 publish_time=video_publish_time))
            db.session.commit()

    except Exception as e:
        print('Error -- {}'.format(str(e)))
        pass