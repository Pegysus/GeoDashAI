import random
import os
import numpy as np
from collections import deque
from learner.config import *
from learner.qnn import QNeuralNetwork
from PIL import Image
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


class QLearning:
    def __init__(self, actions, chk_path=CHK_PATH, save=True, restore=False):
        self.actions = actions
        self.nn = QNeuralNetwork(len(actions))

        self.explore_rate = EXPLORE_START
        self.explore_red = (EXPLORE_START - EXPLORE_END) / float(EXPLORE_TIME - REPLAY_START_SIZE + 1)
        self.iter = -1
        self.num_actions = 0
        self.action_rewards = 0

        self.chk_path = chk_path
        self.save = save

        open(LOG_PATH, 'w').close()

        self.transitions = deque(maxlen=REPLAY_MAX_SIZE)
        print('transitions:', self.transitions)

    def _normalize_frame(self, frame):
        return np.reshape(np.mean(np.array(Image.fromarray(frame).resize(size=(FRAME_HEIGHT, FRAME_WIDTH))), axis=2),
                          (FRAME_HEIGHT, FRAME_WIDTH, 1))

    def _preprocess(self, frame):
        new_frame = self._normalize_frame(frame)
        if not len(self.transitions):
            return np.repeat(new_frame, STATE_FRAMES, axis=2)
        else:
            return np.concatenate((new_frame, self.transitions[-1]['state_in'][:, :, -(STATE_FRAMES-1):]), axis=2)

    def _remember_transition(self, pre_frame, action, terminal):\
        self.transitions.append({'state_in': pre_frame, 'action': self.actions.index(action), 'terminal': terminal})

    def _observe_result(self, resulting_state, reward):
        if len(self.transitions):
            self.transitions[-1]['reward'] = reward
            self.transitions[-1]['state_out'] = resulting_state

    def _is_burning_in(self):
        return len(self.transitions) < REPLAY_START_SIZE

    def explore(self):
        if not self._is_burning_in() and self.explore_rate > EXPLORE_END:
            self.explore_rate = max(self.explore_rate - self.explore_red, EXPLORE_END)
        return random.random() < self.explore_rate or self._is_burning_in()

    def _best_action(self, frame):
        return self.actions[np.argmax(self.nn.compute_q_value(frame))]

    def _random_action(self):
        return self.actions[int(random.random() * len(self.actions))]

    def _compute_target_reward(self, trans):
        target_reward = trans['reward']
        if not trans['terminal']:
            target_reward += DISCOUNT * np.amax(self.nn.compute_q_value(trans['state_out']))

    def step(self, frame, reward, terminal, score_ratio=None):
        self.iter += 1

        if self.iter % LOG_FREQ == 0:
            self._log(score_ratio)

        if self.iter % ACTION_REPEAT != 0:
            self.action_rewards += reward
            return [self.transitions[-1]['action']]

        proc_frame = self._preprocess(frame)
        self._observe_result(proc_frame, self.action_rewards)

        if self.save and self.iter % SAVE_FREQ == 0:
            self._save()

        if not self._is_burning_in() and self.actions % UPDATE_FREQ == 0:
            minibatch = random.sample(self.transitions, BATCH_SIZE)
            batch_frames = [trans['state_in'] for trans in minibatch]
            batch_actions = [trans['action'] for trans in minibatch]
            batch_targets = [self._compute_target_reward(trans) for trans in minibatch]
            self.nn.update(batch_frames, batch_actions, batch_targets)

        action = self._random_action() if self.explore() else self._best_action(proc_frame)
        self.num_actions += 1

        self._remember_transition(proc_frame, action, terminal)
        self.action_rewards = 0

        return [action]

    def _log(self, score_ratio=None):
        print(f'Iteration: {self.iter}')
        if self._is_burning_in() or len(self.transitions) < REPLAY_MAX_SIZE:
            print(f'Replay capacity: {len(self.transitions)} (burn is '
                  f'{"not done)" if self._is_burning_in() else "done)"}')
        if self.explore_rate > EXPLORE_END and not self._is_burning_in():
            print(f'Exploration rate: {self.explore_rate} ({"not" if self._is_burning_in() else "still"} annealing)')
        if not self._is_burning_in():
            print(f"Sample Q output: {self.nn.compute_q_value(self.transitions[-1]['state_in'])}")
        if score_ratio:
            print(f'Score ratio: {score_ratio}')
        print()

        if self.iter % LOG_WRITE_FREQ == 0:
            open(LOG_PATH, 'a').write(str(score_ratio) + '\n')

    def _save(self):
        if not os.path.exists(os.path.dirname(self.chk_path)):
            os.makedirs(os.path.dirname(self.chk_path))

        self.nn.saver.save(self.nn.session, self.chk_path, global_step=self.iter)

    def _restore(self):
        model_path = tf.train.get_checkpoint_state(self.chk_path).model_checkpoint_path
        self.iter = int(model_path[(model_path.rfind('-')+1):]) - 1

        self.explore_rate = max(EXPLORE_END, EXPLORE_START - self.explore_red * self.iter / 4)

        self.nn.saver.restor(self.nn.session, model_path)
