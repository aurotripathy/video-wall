"""
Predict on extracted features
"""
# from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, CSVLogger
from tensorflow.contrib.keras.python.keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, CSVLogger
from models import ResearchModels
from data import DataSet
import time
import os.path
from pudb import set_trace
# from keras.models import load_model
from tensorflow.contrib.keras.python.keras.models import load_model
import numpy as np
import glob
import random
import time


def read_remove_list():
    with open('remove_list.txt') as f:
        list = f.readlines()
    return [x.strip() for x in list]


class Predict():
    def __init__(self, epoch=25, val_loss=1.174, model_type='lstm', seq_length=40, data_type='features'):
        # model can be one of lstm, lrcn, mlp, conv_3d, c3d
        self.model_type = model_type
        self.seq_length = seq_length
        self.data_type = data_type
        filepath=os.path.join('..', 'data', 'checkpoints', model_type + '-' + data_type + '.{:03d}-{:.3f}.hdf5'.format(epoch, val_loss))
        print('Loading the model:', filepath)
        model = load_model(filepath)

        # Get the data and process it.
        self.data = DataSet(seq_length=seq_length, class_limit=None)

        # Get the model.
        print("Model Type:", model_type)
        self.rm = ResearchModels(len(self.data.classes), self.model_type, self.seq_length, filepath)

        # read the video IDs
        self.all_video_ids = sorted([os.path.basename(name).split('.webm')[0] for name in glob.glob('../*/*/*.webm')])
        remove_list = read_remove_list()
        for item in remove_list:
            self.all_video_ids.remove(item)

        self.showing_ids = []

    def get_videos_ids(self, count=12):
        # pick some at random to display
        self.showing_ids = random.sample(self.all_video_ids, count)
        # self.showing_ids = self.all_video_ids[2000:2000+count]
        return self.showing_ids
        
    def predict_video_id(self, video_id, top_N=2):
        sample = self.data.get_frames_by_filename(video_id, self.data_type)
        if sample is not None:
            prediction = self.rm.model.predict(np.expand_dims(sample, axis=0))
            return(self.data.get_top_N_from_prediction(np.squeeze(prediction, axis=0)))
        else:
            return([])

    def predict_all_showing_ids(self):
        predictions = []
        for video_id in self.showing_ids:
            prediction = self.predict_video_id(video_id)
            predictions.append({"id": video_id, "label": prediction})
        return predictions

    def get_all_video_ids(self):
        return self.all_video_ids
# Unit test
def main():
    predict = Predict()

    for video_id in predict.get_all_video_ids():
        predicted = predict.predict_video_id(video_id)
        # print('Predicted', ':', predicted)
        if len(predicted) == 0:
            print('ERROR, Empty prediction for video ID', video_id)

if __name__ == '__main__':
    main()