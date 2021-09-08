import socket
from concurrent.futures import ThreadPoolExecutor


HOST = "localhost"
PORT = 3021

executer = ThreadPoolExecutor(max_workers = 32)
routes = list()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

def request_parser(request_raw):
    lines = request_raw.split('\r\n')
    method, uri, http_version = lines[0].split(' ')
    return {
        'method': method,
        'uri': uri,
        'http_version': http_version,
        'message_body': lines[-1],
    }

def response_builder(http_version, status_code, reason_phrase, message_body):
    return f'''{http_version} {status_code} {reason_phrase}

    {message_body}
    '''

def response_handler(request):
    for route in routes:
        if route['path'] == request['uri'] and route['method'] == request['method']:
            message_body = route['function'](request['message_body'])
            return response_builder(request['http_version'], '200', 'OK', message_body)

    return response_builder(request['http_version'], '404', 'Not Found', f'<h1>Seu {request["uri"]} com o método {request["method"]} não foi encontrado</h1>')

def handler_connection(connection, address):
    request_raw = connection.recv(4096).decode('utf-8')
    request = request_parser(request_raw)
    response = response_handler(request)
    connection.sendall(response.encode('utf-8'))
    connection.close()


def route(path, method):
    def wrapper(function):
        routes.append({
            'path': path,
            'method': method,
            'function': function,
        })

        return function

    return wrapper

###    --- Routes ---- ¨$&@*)#$

value = 'aopa!'

@route(path='/', method='GET')
def index(message_body):
    return f'<h1>{value}</h1>'

@route(path='/photos', method='GET')
def photos(message_body):
    return '<img src="https://w7.pngwing.com/pngs/921/373/png-transparent-kyary-pamyu-pamyu-youtube-funny-face-musician-meme-joke-musician-meme-girl-thumbnail.png"></img>'

@route(path='/echo', method='POST')
def echo(message_body):
    return f'<h2>{message_body}</h2>'

@route(path='/', method='PUT')
def update(message_body):
    global value
    value = message_body
    return 'Foi atualizado with sucesso'


while True:
    conn, addr = s.accept()
    executer.submit(handler_connection, conn, addr)
