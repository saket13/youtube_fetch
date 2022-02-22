from flask import request, jsonify
from project import app, db, celery_app
from project.models import Video


@app.route('/videos')
def fetch_videos():
    page = request.args.get('page', 1, type = int)
    limit = request.args.get('limit', 5, type = int)

    response_dict = {
        'success' : False,
        'results' : [],
        'count' : 0
    }

    try:
        videos = Video.query.paginate(page = page, per_page =limit)
        paginated_videos =(videos.items)
    
        results = [{
            'video_id':video.video_id,
            'title':video.title,
            'description':video.description,
            'thumbnail' : video.thumbnail,
            'channel_title' : video.channel_title,
            'publish_time' : video.publish_time
        } for video in paginated_videos]

        response_dict.update({
            'success' : True,
            'error' : None,
            'results' : results,
            'count' : len(paginated_videos)
        })
    except Exception as e:
        response_dict.update({
            'error' : str(e)
        })

    return response_dict