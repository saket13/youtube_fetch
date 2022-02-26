import json
import requests
from datetime import datetime, timedelta

from project.models import Video
from project.es_utils import push_data_to_es
from project import app, db, celery_app, cache
from project.utils import convert_iso_to_python, convert_python_to_iso

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
        # Latest publish time will be used for publishAfter param in Youtube data API
        latest_publish_time = datetime.now() - timedelta(minutes=30)

        # If any entity exists in DB, change publish after to entity's publish time to fetch latest videos
        latest_entity = Video.query.order_by(Video.publish_time.desc()).limit(1).all()
        if len(latest_entity):
            latest_publish_time = latest_entity[0].publish_time
            
        # Youtube data API accepts date time in ISO format only
        latest_publish_time_iso = convert_python_to_iso(latest_publish_time)

        # Update publishedAfter param
        search_params.update({'publishedAfter' : latest_publish_time_iso})
        
        no_of_keys = int(app.config['YOUTUBE_DATA_API_KEYS_NUM'])
        key_to_be_used = None
        for itr in range(no_of_keys):
            cached_key_result = cache.get('/keys-status/'+'YOUTUBE_DATA_API_KEY_'+str(itr))
            if cached_key_result:
                print(cached_key_result)
                if cached_key_result.get('status') == 'active':
                    key_to_be_used = 'YOUTUBE_DATA_API_KEY_' + str(itr)
                    search_params.update({'key' : app.config[key_to_be_used]})
                    break

        if key_to_be_used is None:
            for itr in range(no_of_keys):
                try:
                    key_to_be_used = 'YOUTUBE_DATA_API_KEY_' + str(itr)
                    search_params.update({'key' : app.config[key_to_be_used]})
                    
                    r = requests.get(search_url, params=search_params)
                    results = r.json().get('items', None)

                    if results:
                        cache.set('/keys-status/'+key_to_be_used, {'status' : 'active'})
                
                except HttpError as e:
                    print('Inactive-{}'.format(key_to_be_used))
                    cache.set('/keys-status/'+key_to_be_used, {'status' : 'expired'})

        else:
            r = requests.get(search_url, params=search_params)
            results = r.json().get('items')
        
        objects = []
        for item in results:
            video_id = item.get('id').get('videoId')
            video_title = item.get('snippet').get('title')
            video_desc = item.get('snippet').get('description')
            video_thumbnail = item.get('snippet').get('thumbnails').get('default').get('url')
            channel_title = item.get('snippet').get('channelTitle')
            video_publish_time_iso = item.get('snippet').get('publishTime')
            video_publish_time = convert_iso_to_python(video_publish_time_iso)
            
            # Create Video objects and append to list for bulk insert
            objects.append(Video(video_id=video_id, 
                                 title=video_title, 
                                 description=video_desc, 
                                 thumbnail=video_thumbnail,
                                 channel_title=channel_title,
                                 publish_time=video_publish_time))

            push_data_to_es('videos', 'title', {'title':video_title})
            push_data_to_es('descriptions', 'description', {'description':video_desc})

        # Bulk Insert objects in DB
        db.session.bulk_save_objects(objects)
        db.session.commit()

    except Exception as e:
        print('Error -- {}'.format(str(e)))
        pass