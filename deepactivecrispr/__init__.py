import os
import tensorflow as tf
import sonnet as snt
import numpy as np
import random

CHARS = [b'A', b'C', b'G', b'T']
CHARS_COUNT = len(CHARS)


class DataSet(object):

    def __init__(self, images, labels, fake_data=False):
        if fake_data:
            self._num_examples = 10000
        else:
            assert images.shape[0] == labels.shape[0], (
                    "images.shape: %s labels.shape: %s" % (images.shape, labels.shape))
            self._num_examples = images.shape[0]

        self._images = images
        self._labels = labels

    @property
    def images(self):
        return self._images

    @property
    def labels(self):
        return self._labels

    @property
    def num_examples(self):
        return self._num_examples


def Ronehot(seq):
    res = np.zeros((23 * 4), dtype=np.uint8)

    seq = np.chararray((23,), buffer=seq.encode('utf-8'))
    seqlen = len(seq)
    arr = np.chararray((seqlen,), buffer=seq)
    for ii, char in enumerate(CHARS):
        res[ii * seqlen:(ii + 1) * seqlen][arr == char] = 1
    ms = res.reshape(4, seqlen).T
    return ms


model_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'HF-train.txt_model2.ckpt')

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

channel_size = [4, 32, 32, 64, 256, 256, 512, 512, 1024, 2]

betas = [None] + [tf.Variable(0.0 * tf.ones(channel_size[i]), name='beta_' + str(i)) for i in
                  range(1, len(channel_size))]
gamma = tf.Variable(1.0 * tf.ones(channel_size[-1]), name='gamma')

e1 = snt.Conv2D(channel_size[1], kernel_shape=[1, 3], name='e_1')
ebn1l = snt.BatchNorm(decay_rate=0.99, offset=False, name='ebn_1l')
e2 = snt.Conv2D(channel_size[2], kernel_shape=[1, 3], stride=2, name='e_2')
ebn2l = snt.BatchNorm(decay_rate=0.99, offset=False, name='ebn_2l')
e3 = snt.Conv2D(channel_size[3], kernel_shape=[1, 3], name='e_3')
ebn3l = snt.BatchNorm(decay_rate=0.99, offset=False, name='ebn_3l')
e4 = snt.Conv2D(channel_size[4], kernel_shape=[1, 3], stride=2, name='e_4')
ebn4l = snt.BatchNorm(decay_rate=0.99, offset=False, name='ebn_4l')
e5 = snt.Conv2D(channel_size[5], kernel_shape=[1, 3], name='e_5')
ebn5l = snt.BatchNorm(decay_rate=0.99, offset=False, name='ebn_5l')
e6 = snt.Conv2D(channel_size[6], kernel_shape=[1, 3], stride=2, name='e_6')
ebn6l = snt.BatchNorm(decay_rate=0.99, offset=False, name='ebn_6l')
e7 = snt.Conv2D(channel_size[7], kernel_shape=[1, 3], name='e_7')
ebn7l = snt.BatchNorm(decay_rate=0.99, offset=False, name='ebn_7l')
e8 = snt.Conv2D(channel_size[8], kernel_shape=[1, 3], padding='VALID', name='e_8')
ebn8l = snt.BatchNorm(decay_rate=0.99, offset=False, name='ebn_8l')
e9 = snt.Conv2D(channel_size[9], kernel_shape=[1, 1], name='e_9')
ebn9l = snt.BatchNorm(decay_rate=0.99, offset=False, name='ebn_9l')
e0 = snt.Conv2D(channel_size[9], kernel_shape=[1, 1], name='e_0')
ebn0l = snt.BatchNorm(decay_rate=0.99, offset=False, name='ebn_0l')
ea = snt.Conv2D(channel_size[9], kernel_shape=[1, 1], name='e_a')
ebnal = snt.BatchNorm(decay_rate=0.99, offset=False, name='ebn_al')

encoder = [None, e1, e2, e3, e4, e5, e6, e7, e8, e9]
encoder_bn_l = [None, ebn1l, ebn2l, ebn3l, ebn4l, ebn5l, ebn6l, ebn7l, ebn8l, ebn9l]

inputs_l = tf.placeholder(dtype=tf.float32, shape=[None, 1, 23, 4])
outputs_raw = tf.placeholder(tf.uint8, shape=[None])
outputs = tf.one_hot(outputs_raw, depth=2)
training = tf.placeholder(dtype=tf.bool)

hl0 = inputs_l
l_lst = [hl0]
hl_lst = [hl0]

for i in range(1, len(channel_size) - 1):
    hl_pre = hl_lst[i - 1]
    pre_l = encoder[i](hl_pre)
    l = encoder_bn_l[i](pre_l, training, test_local_stats=False)
    hl = tf.nn.relu(l + betas[i])
    l_lst.append(l)
    hl_lst.append(hl)

hl_m1 = hl_lst[-1]
pre_l_last = encoder[-1](hl_m1)
l_last = encoder_bn_l[-1](pre_l_last, training, test_local_stats=False)
l_last = gamma * l_last + betas[-1]
hl_last = tf.nn.softmax(l_last)
l_lst.append(l_last)
hl_lst.append(hl_last)
prob = hl_last

saver = tf.train.Saver()
saver.restore(sess, model_path)


def load_weights():
    pass


def calculate_spacer(spacer):
    X_train = np.zeros((1, 1, 23, 4))
    X_train[0][0] = Ronehot(spacer)

    propred = sess.run(prob, feed_dict={inputs_l: X_train, training: False})
    return propred[0][0][0][1]
