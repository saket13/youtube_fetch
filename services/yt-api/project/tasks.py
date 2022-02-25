import json
import requests
from project.models import Video
from project import app, db, celery_app
from datetime import datetime, timedelta
from project.utils import convert_iso_to_python, convert_python_to_iso, store_record

@celery_app.task
def fetch():
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    
    search_params = {
        'part' : 'snippet',
        'q' : 'science',
        'maxResults' : 10,
        'type' : 'video'
    }

    try:
        latest_publish_time = datetime.now() - timedelta(minutes=30)
        latest_entity = Video.query.order_by(Video.publish_time.desc()).limit(1).all()
        if len(latest_entity):
            latest_publish_time = latest_entity[0].publish_time
            
        latest_publish_time_iso = convert_python_to_iso(latest_publish_time)
        search_params.update({'publishedAfter' : latest_publish_time_iso,
                               'key' : app.config['YOUTUBE_DATA_API_KEY']}) 

        r = requests.get(search_url, params=search_params)
        results = r.json()['items']
        
        objects = []
        for item in results:
            video_id = item.get('id').get('videoId')
            video_title = item.get('snippet').get('title')
            video_desc = item.get('snippet').get('description')
            video_thumbnail = item.get('snippet').get('thumbnails').get('default').get('url')
            channel_title = item.get('snippet').get('channelTitle')
            video_publish_time_iso = item.get('snippet').get('publishTime')
            video_publish_time = convert_iso_to_python(video_publish_time_iso)
            
            objects.append(Video(video_id=video_id, 
                                 title=video_title, 
                                 description=video_desc, 
                                 thumbnail=video_thumbnail,
                                 channel_title=channel_title,
                                 publish_time=video_publish_time))

            store_record('videos', 'title', {'title':video_title})
            store_record('descriptions', 'description', {'description':video_desc})

        db.session.bulk_save_objects(objects)
        db.session.commit()

    except Exception as e:
        print('Error -- {}'.format(str(e)))
        pass