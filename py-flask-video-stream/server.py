
from __future__ import print_function

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import logging
import os
import re
import sys
import time
import pprint
import random

import mimetypes
from flask import Response, render_template
from flask import Flask
from flask import send_file
from flask import request
from flask import jsonify

from pudb import set_trace

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Predict import Predict

# set_trace()
predict = Predict()

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

app = Flask(__name__)

VIDEO_PATH = '/video'
VID_COUNT = 12

MB = 1 << 20
BUFF_SIZE = 10 * MB


video_filenames = os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'videos'))
LOG.debug('Video files: {}'.format(video_filenames))

@app.route('/show')
def home():
    LOG.debug('Rendering home page')
    id_list = predict.get_videos_ids(VID_COUNT)
    id_list = [id + '.webm' for id in id_list]  # append .webm
    # id_list = [i for i in range(VID_COUNT)]
    # random.shuffle(id_list)
    
    response = render_template(
        'index.html', 
        video=VIDEO_PATH,
        id_list=id_list,
    )
    return response

def partial_response(path, start, end=None):
    LOG.debug('Requested: %s, %s', start, end)
    file_size = os.path.getsize(path)

    # Determine (end, length)
    if end is None:
        end = start + BUFF_SIZE - 1
    end = min(end, file_size - 1)
    end = min(end, start + BUFF_SIZE - 1)
    length = end - start + 1

    # Read file
    with open(path, 'rb') as fd:
        fd.seek(start)
        bytes = fd.read(length)
    assert len(bytes) == length

    response = Response(
        bytes,
        206,
        mimetype=mimetypes.guess_type(path)[0],
        direct_passthrough=True,
    )
    response.headers.add(
        'Content-Range', 'bytes {0}-{1}/{2}'.format(
            start, end, file_size,
        ),
    )
    response.headers.add(
        'Accept-Ranges', 'bytes'
    )
    LOG.info('Response: %s', response)
    LOG.info('Response: %s', response.headers)
    return response

def get_range(request):
    range = request.headers.get('Range')
    LOG.info('Requested: %s', range)
    m = re.match('bytes=(?P<start>\d+)-(?P<end>\d+)?', range)
    if m:
        start = m.group('start')
        end = m.group('end')
        start = int(start)
        if end is not None:
            end = int(end)
        return start, end
    else:
        return 0, None
    

@app.route('/video/<id>/')
def video(id):
    LOG.debug('Rendering video ID:{}'.format(id))
    # path = 'videos/v_TennisSwing_g01_c01.webm'

    # convert video ID to a file name
    # path = os.path.join('videos', video_filenames[int(id)])
    path = os.path.join('videos', id)
    LOG.debug('Filename to render: {}'.format(path))


    start, end = get_range(request)
    return partial_response(path, start, end)


@app.route('/classify_all/')
def classify():
    LOG.debug('Enter route classify_all')
    # dummy_dict = [{"id":str(i), "label":"dummy"+str(i)} for i in range(VID_COUNT)]
    # LOG.debug(dummy_dict)
    predictions = predict.predict_all_showing_ids()
    LOG.debug(predictions)
    # return jsonify(dummy_dict)
    return jsonify(predictions)


@app.route('/loop/')
def show_classify():  # in a loop
    LOG.debug('Showing videos and classifying at the same time')
    id_list = predict.get_videos_ids(VID_COUNT)
    id_list = [id + '.webm' for id in id_list]  # append .webm
    # id_list = [i for i in range(VID_COUNT)]
    # random.shuffle(id_list)
    predictions = predict.predict_all_showing_ids()  # contains id and label
    predictions = [prediction['label'] for prediction in predictions]  # just label
    predictions = [''.join(prediction) for prediction in predictions]  # as string
    print(predictions)
        
    LOG.debug(predictions)
    
    response = render_template(
        'auto_run_index.html', 
        video=VIDEO_PATH,
        id_list=id_list,
        predictions=predictions,
    )
    return response


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    HOST = '0.0.0.0'
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(9000)
    IOLoop.instance().start()

    # Standalone
    app.run(host=HOST, port=9000, debug=True)
