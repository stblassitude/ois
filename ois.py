#!/usr/bin/env python
import json
import paho.mqtt.client as mqtt
import asyncio
import tornado.escape
import tornado.locks
import tornado.web
import os.path
import uuid

from asyncio_mqtt import Client, MqttError

class OIS:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set("onon", "hybrid")
        self.client.connect('diesel.lassitu.de', 1883)
        self.client.loop()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected")
        client.subscribe("stat/ois/RESULT")
        pass

    def on_message(self, client, userdata, msg):
        # print(msg.topic+" "+str(msg.payload))
        m = json.loads(msg.payload)
        try:
            action = m["Button1"]["Action"]
            print(f"action: {action}")
            client.publish("cmnd/ois/POWER", "OFF")
        except KeyError:
            # ignore message
            pass

    def start(self):
        self.client.loop_start()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages="foo")


class OnHandler(tornado.web.RequestHandler):
    def initialize(self, ois:OIS) -> None:
        self.ois = ois

    def get(self):
        self.ois.client.publish("cmnd/ois/POWER", "ON")
        self.render("index.html", messages="foo")


async def main():
    ois = OIS()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/on", OnHandler, {'ois':ois})
        ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=True,
    )
    app.listen(8080)
    # async with Client("diesel.lassitu.de", username="onon", password="hybrid") as client:
    #     global gclient
    #     gclient = client
    #     async with client.filtered_messages("stat/ois/RESULT") as messages:
    #         await client.subscribe("stat/ois/RESULT")
    #         async for message in messages:
    #             print(message.payload.decode())
    #             await client.publish("cmnd/ois/POWER", "ON")
    ois.start()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())