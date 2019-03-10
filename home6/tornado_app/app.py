import json
import os

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.options
from tornado.log import enable_pretty_logging

from db import DbController


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/index.html', name='', error='', room='')

    def post(self):
        name = self.get_body_argument('name')
        room = self.get_body_argument('room')
        if name == 'ADMIN' and room == '11':
            return self.redirect('/admin')
        elif int(room) not in range(1, 11):
            error = 'Недопустимый номер комнаты!'
        elif WebSocketHandler.check_users(room, name):
            error = 'Имя уже занято!'
        else:
            return self.redirect(f'/{room}?name={name}')
        self.render('templates/index.html', name=name, error=error, room=room)


class RoomHandler(tornado.web.RequestHandler):
    def get(self, room):
        data = DbController.get_room_messages(room)
        messages = []
        for item in data:
            messages.append((item.name, item.text))
        name = self.get_query_argument('name')
        self.render('templates/room.html', room=room, data=data, name=name)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    users = {str(i): dict() for i in range(1, 11)}

    @classmethod
    def check_users(cls, room, name):
        for data in cls.users[room]:
            if name in data:
                return True
        return False

    def open(self):
        room = self.get_query_argument('room')
        name = self.get_query_argument('name')
        self.users[room][name] = self
        print('socket users: ', self.users)
        for user in self.users[room].values():
            user.write_message({'type': 'online', 'value': len(self.users[room])})

    @classmethod
    def send_message(cls, message):
        room = message['room']
        name = message['name']
        text = message['text']
        for user in cls.users[str(room)].values():
            user.write_message({'type': 'message', 'name': name, 'text': text})

    def on_message(self, message):
        message = json.loads(message)
        DbController.add_message(name=message['name'], text=message['text'], room=message['room'])
        self.send_message(message)

    def on_close(self):
        room = self.get_query_argument('room')
        name = self.get_query_argument('name')
        del self.users[room][name]
        for user in self.users[room].values():
            user.write_message({'type': 'online', 'value': len(self.users[room])})

    def check_origin(self, origin):
        return True


class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        return self.render('templates/admin.html', result='')

    def post(self):
        room = self.get_body_argument('room')
        if int(room) not in range(1, 11):
            result = 'Неверное название комнаты.'

        elif self.get_argument('clear', None) is not None:
            DbController.clear_room(int(room))
            result = f'Комната {room} очищена от сообщений.'
            for user in WebSocketHandler.users[room].values():
                user.write_message({'type': 'admin-clear'})

        elif self.get_argument('kick', None) is not None:
            result = f'Комната {room} перезагружена.'
            for user in WebSocketHandler.users[room].values():
                user.write_message({'type': 'admin-kick'})

        return self.render('templates/admin.html', result=result)


def make_app():
    return tornado.web.Application(handlers=[
        (r'/', IndexHandler),
        (r'/ws', WebSocketHandler),
        (r'/admin', AdminHandler),
        (r'/(\d+)', RoomHandler)])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    enable_pretty_logging()
    tornado.ioloop.IOLoop.current().start()
