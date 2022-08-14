# Parameters used in the learner and graph of the NN

# learning rate of network
LEARNING_RATE = 1e-6

# frame of the NN
FRAME_HEIGHT, FRAME_WIDTH = (84, 84)
STATE_FRAMES = 4

# exploration parameters, probability of exploring at the start and end (linearly decreasing) and amount of time
# or steps to explore before NN reaches its "local minima/maxima"
EXPLORE_START = 1
EXPLORE_END = 0.05
EXPLORE_TIME = 1e6

# discount factor (gamma)
DISCOUNT = 0.9

BATCH_SIZE = 32

ACTION_REPEAT = 4

REPLAY_START_SIZE = 50000
REPLAY_MAX_SIZE = 100000

UPDATE_FREQ = 4

LOG_FREQ = 10000
LOG_WRITE_FREQ = 10000
LOG_IN_A_ROW = 1
SAVE_FREQ = 500000
LOG_PATH = 'deep_q_log.txt'

CHK_PATH = './deep-q-model/'
