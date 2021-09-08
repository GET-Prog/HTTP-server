from server import route

value = 'aopa!'

@route(path='/', method='GET')
def index():
    return f'<h1>{value}</h1>'

@route(path='/photos', method='GET')
def photos():
    return '<img src="https://w7.pngwing.com/pngs/921/373/png-transparent-kyary-pamyu-pamyu-youtube-funny-face-musician-meme-joke-musician-meme-girl-thumbnail.png"></img>'

@route(path='/echo', method='POST')
def echo(message_body):
    return f'<h2>{message_body}</h2>'

@route(path='/', method='PUT')
def update(message_body):
    value = message_body
    return 'Foi atualizado with sucesso'
