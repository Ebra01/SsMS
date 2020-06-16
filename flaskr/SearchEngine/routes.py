from flask import Blueprint, jsonify, request, abort
from .utils import handleSearch

search = Blueprint('search', __name__)


@search.route('/api/search', methods=['POST'])
def searchEngine():
    # this request can be empty
    req = request.get_json()

    # These can be empty too (searchKey is default to 'all')
    searchKey = req.get('searchKey')
    searchTerm = req.get('search')

    results = {}

    try:
        if searchTerm and searchKey:
            results = handleSearch(searchTerm, searchKey)
    except Exception as e:
        print(e)
        abort(400, e)

    return jsonify({
        'results': results,
        'success': True
    })
