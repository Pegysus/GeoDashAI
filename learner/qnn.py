from learner.config import *
import learner.graph as g
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


class QNeuralNetwork:
    def __init__(self, output_w):
        self.in_graph, self.out_graph = g.gen_nn(output_w)

        self.actions = tf.placeholder(tf.int32)
        self.pred_rewards = tf.placeholder(tf.float32)
        act_reward = tf.gather_nd(self.out_graph, self.actions)
        self.loss = tf.reduce_mean(tf.square(self.pred_rewards - act_reward))
        self.optimizer = tf.train.AdamOptimizer(LEARNING_RATE).minimize(self.loss)

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())

        self.saver = tf.train.Saver()

    def __del__(self):
        self.session.close()

    def compute_q_value(self, in_nn):
        return self.session.run(self.out_graph, feed_dict={self.in_graph: [in_nn]})[0]

    def update(self, batch_frames, batch_actions, batch_targets):
        return self.session.run(
            [self.optimizer, self.loss],
            feed_dict={
                self.in_graph: batch_frames,
                self.actions: [act for act in enumerate(batch_actions)],
                self.pred_rewards: batch_targets
            }
        )[1]
