# pip install 'pubnub>=4.0.8'

from pprint import pprint

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'xxxxxxxxxxxxxxxxxxxx'
pnconfig.publish_key = 'xxxxxxxxxxxxxxxxxxxx'

pubnub = PubNub(pnconfig)

channel_name = 'aiception-channel'
payload = {
    "action": "detect-object",
    "body": {
        "image_url": "http://static.boredpanda.com/blog/wp-content/uploads/2016/01/cute-squirrel-photography-361__700.jpg",
        "async": False
    }
}


def on_connected():
    pubnub.publish().channel(channel_name).message(
        payload).async(callback)


def callback(response, status):
    if not status.is_error():
        pass
    else:
        print("published with error")


class MySubscribeCallback(SubscribeCallback):

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            on_connected()

    def message(self, pubnub, message):
        pprint(message.message)
        # print(message.channel)
        # print(message.publisher)
        # print(message.subscription)
        # print(message.timetoken)
        # print(message.user_metadata)


pubnub.add_listener(MySubscribeCallback())

pubnub.subscribe().channels(channel_name).execute()
