import logging
from pprint import pformat
import requests
import time


logger = logging.getLogger('aiception')
FORMAT = '%(message)s'
logging.basicConfig(level=logging.WARNING, format=FORMAT)
logging.getLogger("requests").setLevel(logging.WARNING)


def face_age(token, image_url):
    data = {'image_url': image_url}
    return callEndpoint("https://aiception.com/api/v2.1/face_age", token, data)


def detect_object(token, image_url):
    data = {'image_url': image_url}
    return callEndpoint("https://aiception.com/api/v2.1/detect_object", token, data, initial_wait=2000)


def detect_object_sync(token, image_url):
    data = {'image_url': image_url, 'async': False}
    r = requests.post("https://aiception.com/api/v2.1/detect_object", auth=(token, 'password is ignored'), json=data)
    return r.json()


def adult_content(token, image_url):
    data = {'image_url': image_url}
    return callEndpoint("https://aiception.com/api/v2.1/adult_content", token, data, initial_wait=2000)


def faces(token, image_url):
    data = {'image_url': image_url}
    return callEndpoint("https://aiception.com/api/v2.1/face", token, data, initial_wait=2000)


def artistic_image(token, image_url, style_url):
    data = {
        'image_url': image_url,
        'style_url': style_url
    }
    return callEndpoint("https://aiception.com/api/v2.1/artistic_image", token, data, initial_wait=50 * 1000, increment_wait=15 * 1000, retries=30)


def callEndpoint(endpoint, token, datapayload, initial_wait=1000, increment_wait=1000, retries=20):

    r = requests.post(endpoint, auth=(
        token, 'password is ignored'), json=datapayload)

    logger.debug('Headers')
    logger.debug(pformat(r.headers))
    logger.debug('Server response to our POST request')
    logger.debug(pformat(r.json()))

    task_url = r.headers['Location']

    # sleep initial_wait
    time.sleep(float(initial_wait) / 1000)

    for _ in range(retries):
        r = requests.get(task_url, auth=(token, 'password is ignored'))
        logger.debug(pformat(r.json()))

        if 'answer' in r.json():
            if isinstance(r.json()['answer'], str):
                logger.debug('not done')
            else:
                logger.debug('done')
                return r.json()

        # sleep increment_wait
        time.sleep(float(increment_wait) / 1000)

    logger.error('could not get the response')
    return None
