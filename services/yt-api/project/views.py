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
        videos = Video.query.order_by(Video.publish_time.desc()).paginate(page = page, per_page = limit)
        paginated_videos =(videos.items)
        results = [video.format() for video in paginated_videos]
    
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

@app.route('/search')
def search_videos():

    query = request.args.get('q', type = str)

    response_dict = {
        'success' : False,
        'results' : []    
    }

    try:
        videos = Video.query.filter(Video.title.ilike("%{}%".format(query)))
        results = [video.format() for video in videos]

        response_dict.update({
            'success' : True,
            'error' : None,
            'results' : results
        })       
    except Exception as e:
        response_dict.update({
            'error' : str(e)
        })

    return response_dict