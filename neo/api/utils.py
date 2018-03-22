import json
import gzip
from functools import wraps

COMPRESS_FASTEST = 1
BASE_STRING_SIZE = 49
MTU_TCP_PACKET_SIZE = 1500
COMPRESS_THRESHOLD = MTU_TCP_PACKET_SIZE + BASE_STRING_SIZE


# @json_response decorator for class methods
def json_response(func):
    """ @json_response decorator adds header and dumps response object """

    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        res = func(self, request, *args, **kwargs)
        response_data = json.dumps(res) if isinstance(res, dict) else res
        request.setHeader('Content-Type', 'application/json')

        if len(response_data) > COMPRESS_THRESHOLD:
            accept_encoding = request.getHeader('Accept-Encoding')
            if accept_encoding:
                encodings = accept_encoding.split(',')

                if 'gzip' in encodings:
                    response_data = gzip.compress(bytes(response_data, 'utf-8'), compresslevel=COMPRESS_FASTEST)
                    request.setHeader('Content-Encoding', 'gzip')
                    request.setHeader('Content-Length', len(response_data))

        return response_data

    return wrapper


# @cors_header decorator to add the CORS headers
def cors_header(func):
    """ @cors_header decorator adds CORS headers """

    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        res = func(self, request, *args, **kwargs)
        request.setHeader('Access-Control-Allow-Origin', '*')
        return res

    return wrapper
