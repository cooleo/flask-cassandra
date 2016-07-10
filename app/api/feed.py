import codecs
import json
from uuid import UUID
from flask import Flask, app, jsonify, abort, request, make_response, url_for
from app.api import api
from app.models.feed import Feed
from app.models.photo import Photo
from app.models.video import Video


def _validate_uuid4(uuid_string):
    """
    Validate that a UUID string is in
    fact a valid uuid4.
    """

    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        return False

    return val.hex == uuid_string


@api.route('/feed/<id>', methods=['GET'])
def get_feed(id):
    """
    Fetch shopping_list
    """

    query = Feed.objects(id=UUID(id))
    if query.count > 0:
        data = {'results': []}
        i = 0
        for instance in query:
            data['results'].append({'id': instance.id,
                                    'title': instance.title,
                                    'slug': instance.slug,
                                    'description': instance.description,
                                    'created_at': instance.created_at})
            i += 1
            if i == query.count():
                return make_response(jsonify({'success': True, 'results': data['results']}), 200)
    else:
        return make_response(jsonify({'success': True, 'results': []}), 204)


@api.route('/feed', methods=['POST'])
def post_feed():
    """
    Insert feed
    """
    data = request.get_json(silent=True)
    type = data['type']
    if type == 1:
        video = data['video']
        title = video['title']
        description = video['description']
        url = video['url']
        v_result = Video.create(title=title, description=description, url=url)

    if type == 2:
        photo = data['photo']
        title = photo['title']
        description = photo['description']
        url = photo['url']
        Photo.create(title=title, description=description, url=url)

    if type == 3:
        article = data['news']

    print(data)

    if 'name' in data and 'description' in data and 'slug' in data:
        name = data['name']
        description = data['description']
        slug = data['slug']
        Feed.create(name=name, description=description, slug=slug)
        return make_response(jsonify({'success': True, 'result': 'Category Created'}), 201)
    else:
        return make_response(jsonify({'success': False, 'result': 'Incomplete parameters'}), 400)
