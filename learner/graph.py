from learner.config import *
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

G_INPUT = 'frame_input'
G_W_CONV1 = 'w_conv1'
G_B_CONV1 = 'b_conv1'
G_W_CONV2 = 'w_conv2'
G_B_CONV2 = 'b_conv2'
G_W_CONV3 = 'w_conv3'
G_B_CONV3 = 'b_conv3'
G_W_FC1 = 'w_fc1'
G_B_FC1 = 'b_fc1'
G_W_FC2 = 'w_fc2'
G_B_FC2 = 'b_fc2'
G_VAL = 'q_value'


def gen_nn(output_w):
    """"""
    in_graph = tf.compat.v1.placeholder(
        tf.float32,
        shape=[None, FRAME_HEIGHT, FRAME_WIDTH, STATE_FRAMES],
        name=G_INPUT
    )

    w_conv1 = _weight_vars([8, 8, STATE_FRAMES, 32], G_W_CONV1)
    b_conv1 = _bias_vars([32], G_B_CONV1)
    conv_1 = tf.nn.relu(_conv2d(in_graph, w_conv1, 4) + b_conv1)

    w_conv2 = _weight_vars([4, 4, 32, 64], G_W_CONV2)
    b_conv2 = _bias_vars([64], G_B_CONV2)
    conv_2 = tf.nn.relu(_conv2d(conv_1, w_conv2, 4) + b_conv2)

    w_conv3 = _weight_vars([3, 3, 64, 64], G_W_CONV3)
    b_conv3 = _bias_vars([64], G_B_CONV3)
    conv_3 = tf.nn.relu(_conv2d(conv_2, w_conv3, 4) + b_conv3)
    conv_3f = tf.reshape(conv_3, [-1, 7744])

    w_fc1 = _weight_vars([7744, 512], G_W_FC1)
    b_fc1 = _bias_vars([512], G_B_FC1)
    fc_1 = tf.nn.relu(tf.matmul(conv_3f, w_fc1) + b_fc1)

    w_fc2 = _weight_vars([512, output_w], G_W_FC2)
    b_fc2 = _bias_vars([output_w], G_B_FC2)
    out_graph = tf.add(tf.matmul(fc_1, w_fc2), b_fc2, name=G_VAL)

    return in_graph, out_graph


def _conv2d(data, weights, stride):
    return tf.nn.conv2d(data, weights, strides=[1, stride, stride, 1], padding='SAME')


def _weight_vars(shape, name):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.01), name=name)


def _bias_vars(shape, name):
    return tf.Variable(tf.constant(0.01, shape=shape), name=name)
