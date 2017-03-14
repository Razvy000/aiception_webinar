from pprint import pprint
import subprocess
import time
import queue

from gpiozero import LED

import boto3

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


# thread safe queue
q = queue.Queue()

# led
led = LED(7)

# pubnub
pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
pnconfig.publish_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

pubnub = PubNub(pnconfig)
channel_name = 'aiception-channel'


def callback(response, status):
    if not status.is_error():
        pass
    else:
        print("published with error")


class QSubscribeCallback(SubscribeCallback):

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            print("connected to pubnub")

    def message(self, pubnub, message):
        q.put(message.message)


# add pubnub listener
pubnub.add_listener(QSubscribeCallback())

# connect to pubnub
pubnub.subscribe().channels(channel_name).execute()

# wait 2 seconds to connect (should use the status)
time.sleep(2)


# s3
client = boto3.client('s3')
bucket = 'raspi-bucket'

state = 'no_squirrel'  # 'captured_squirrel'

for _ in range(10):
    print()
    print('state is ' + state)

    if state == 'no_squirrel':
        # wait a while
        time.sleep(5)

        # capture image
        print("take image")
        subprocess.call("raspistill -w 400 -h 300 --roi 0.45,0.4,0.3,0.3" +
                        "--nopreview --vflip --hflip --timeout 1000 --output image.jpg",
                        shell=True)

        # upload to s3
        print("upload image")
        key = 'one_image.jpg'
        client.upload_file('image.jpg', bucket, key,
                           ExtraArgs={'ACL': 'public-read'})
        file_url = '%s/%s/%s' % (client.meta.endpoint_url, bucket, key)

        # publish to pubnub
        print("publish")
        payload = {
            "action": "detect-object",
            "body": {
                "image_url": file_url,
                "async": False
            }
        }
        pubnub.publish().channel(channel_name).message(payload).async(callback)

        # get from queue
        msg = None
        while not q.empty():
            try:
                msg = q.get(block=False)  # timeout=None
            except queue.Empty:
                pass

        # pprint(msg)
        if not msg or 'aiceptionResponse' not in msg:
            continue

        print("receive")
        main_obj = msg['aiceptionResponse']['answer'][0]
        label = main_obj[0]
        score = main_obj[1]
        if 'orange' in label:
            print("   we found an orange!")
            state = 'captured_squirrel'
        if 'fox squirrel' in label:
            print("   we found a squirrel!!!")
            state = 'captured_squirrel'

    elif state == 'captured_squirrel':

        # close door
        print("close door")
        led.on()

        # do a 1o seconds recording
        print("recording squirrel")
        subprocess.call(
            "raspivid --timeout 10000 --output squirrel.avi", shell=True)
        print("recording done")

        ######################################################################
        # HOMEWORK
        # upload movie to s3 bucket
        # send mobile notification using pubnub with the video / image link
        ######################################################################

        # open door and let squirrel free
        print("open door")
        led.off()

        # clear the message queue
        q.queue.clear()

        state = 'no_squirrel'
    else:
        print('we have an error')

# unsubscribe from pubnub
pubnub.unsubscribe().channels(channel_name).execute()
