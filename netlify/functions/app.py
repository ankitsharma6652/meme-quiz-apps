import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app import app

def handler(event, context):
    """Netlify serverless function handler"""
    from werkzeug.wrappers import Request, Response
    from io import BytesIO
    
    # Convert Netlify event to WSGI environ
    environ = {
        'REQUEST_METHOD': event.get('httpMethod', 'GET'),
        'SCRIPT_NAME': '',
        'PATH_INFO': event.get('path', '/'),
        'QUERY_STRING': event.get('queryStringParameters', ''),
        'SERVER_NAME': 'netlify',
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': BytesIO(event.get('body', '').encode('utf-8')),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # Add headers
    headers = event.get('headers', {})
    for key, value in headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = f'HTTP_{key}'
        environ[key] = value
    
    # Call Flask app
    response_data = []
    def start_response(status, response_headers):
        response_data.append(status)
        response_data.append(response_headers)
    
    app_response = app(environ, start_response)
    body = b''.join(app_response).decode('utf-8')
    
    # Convert to Netlify response format
    status_code = int(response_data[0].split()[0])
    headers_dict = {k: v for k, v in response_data[1]}
    
    return {
        'statusCode': status_code,
        'headers': headers_dict,
        'body': body
    }
