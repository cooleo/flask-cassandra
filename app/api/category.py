import codecs
import json
from uuid import UUID
from flask import Flask, app, jsonify, abort, request, make_response, url_for
from app.api import api
from app.models.category import Category


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


@api.route('/category/<id>', methods=['GET'])
def get_category(id):
    """
    Fetch shopping_list
    """

    query = Category.objects(user_id=int(id))
    if query.count > 0:
        data = {'results': []}
        i = 0
        for instance in query:
            data['results'].append({'id': instance.id,
                                    'name': instance.name,
                                    'slug': instance.slug,
                                    'description': instance.description,
                                    'created_at': instance.created_at})
            i += 1
            if i == query.count():
                return make_response(jsonify({'success': True, 'results': data['results']}), 200)
    else:
        return make_response(jsonify({'success': True, 'results': []}), 204)


@api.route('/category', methods=['POST'])
def post_category():
    """
    Insert shopping_list
    """
    data = request.get_json(silent=True)
    print(data)

    if 'name' in data and 'description' in data and 'slug' in data:
        name = data['name']
        description = data['description']
        slug = data['slug']

        Category.create(name=name, description=description, slug=slug)
        return make_response(jsonify({'success': True, 'result': 'Category Created'}), 201)
    else:
        return make_response(jsonify({'success': False, 'result': 'Incomplete parameters'}), 400)
