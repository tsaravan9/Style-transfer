# Tornado Libraries
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from PIL import Image
import io
import numpy
import os
import sys
import time
import numpy as np
import pandas as pd

import torch
from torch.optim import Adam
from torch.autograd import Variable
from torch.utils.data import DataLoader

from torchvision import datasets
from torchvision import transforms

import utils
from net import Net, Vgg16


style_images_path = 'images/museum_styles/'
dataset_df = pd.read_csv('dataset.csv')

style_model = Net(ngf=128)
style_model.load_state_dict(torch.load(model), False)
cuda = torch.cuda.is_available()

if cuda:
    style_model.cuda()
    content_image = content_image.cuda()
    style = style.cuda()


def check_paths(args):
    try:
        if not os.path.exists(args.vgg_model_dir):
            os.makedirs(args.vgg_model_dir)
        if not os.path.exists(args.save_model_dir):
            os.makedirs(args.save_model_dir)
    except OSError as e:
        print(e)
        sys.exit(1)


def evaluate(raw_content_image, raw_content_size, style_image, style_size, cuda, output):
    content_image = utils.tensor_load_rgbimage(
        raw_content_image, size=raw_content_size, keep_asp=True)
    content_image = content_image.unsqueeze(0)
    style = utils.tensor_load_rgbimage(style_image, size=style_size)
    style = style.unsqueeze(0)
    style = utils.preprocess_batch(style)

    style_v = Variable(style)

    content_image = Variable(utils.preprocess_batch(content_image))
    style_model.setTarget(style_v)

    output = style_model(content_image)
    transfer_image = utils.tensor_save_bgrimage(
        output.data[0], output_image, cuda)
    return transfer_image


class UploadHandler(tornado.web.RequestHandler):

    def post(self):
        file = self.request.files['file'][0]
        style_id = self.get_argument('style_id')
        content = file['body']
        image = (io.BytesIO(content))
        print(image)
        image_path = style_images_path + style_id + '.jpg'
        if os.path.exists(image_path):
            result_image = evaluate(
                image, 512, image_path, 512, cuda, 'output')
            response = {}
            response['style_image'] = str(numpy.asarray(image))
            self.write(response)
        else:
            self.write({'Response': 'Image not Found'})


class DatasetHandler(tornado.web.RequestHandler):

    def get(self):
        # print(dataset_df.head())
        dataset = {}
        dataset['images'] = []
        # print(dataset_df)
        for index, row in dataset_df.iterrows():
            item={}
            item['Title']=row['Title']
            item['Database ID']=row['Database ID']
            item['Link']=row['Link']
            dataset['images'].append(item)
        self.write(dataset)
                
app = tornado.web.Application([
    (r'/upload', UploadHandler),
    (r'/dataset', DatasetHandler)
], debug=True)

app.listen(8001)
tornado.ioloop.IOLoop.instance().start()
