import itertools
import numpy as np
import simplejson as json
import os
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Dropout
from keras.layers import LSTM

batch_size = 2
timesteps = 1
nb_epoch = 20
final_test = None
final_test_out = None


def train(turn):
    global model
    global final_test
    global final_test_out

    X_train = []
    X_test = []
    y_train = []
    y_test = []
    with open("match_prepared.dat", 'r') as f:
        with open("match_out_prepared.dat", 'r') as f2:
            timesteps_tr = []
            timesteps_te = []
            for line_tr, line_te in itertools.izip(f, f2):
                steps = []
                for num in line_tr.strip().split():
                    steps.append(float(num))
                if len(timesteps_tr) != 14000:
                    timesteps_tr.append([steps] * timesteps)
                    y_train.append([int(line_te.strip())])
                elif len(timesteps_te) != 4554:
                    timesteps_te.append([steps] * timesteps)
                    y_test.append([int(line_te.strip())])

    X_train.extend(timesteps_tr)
    X_test.extend(timesteps_te)
    X_train, X_test = np.array(X_train), np.array(X_test)

    turn[0] += 1

    y_train = np.array(y_train)
    y_test = np.array(y_test)
    model = load_model("cs_model_test1.h5")
    for i in range(nb_epoch):
        print "Epoch: {}".format(str(i + 1))
        model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=1, verbose=2)
        sc = model.evaluate(X_test, y_test, batch_size=batch_size, verbose=0)
        print "Epoch Success:", sc[1]
    if final_test is None:
        final_test = np.array(X_test)
    else:
        final_test = np.concatenate((final_test, X_test))
    if final_test_out is None:
        final_test_out = np.array(y_test)
    else:
        final_test_out = np.concatenate((final_test_out, y_test))
    # score = model.evaluate(X_test, y_test, verbose=0)
    # print('Test score:', score[0])
    # print('Test accuracy:', score[1])
    model.save("cs_model_test1.h5")


with open(os.path.abspath('..' + os.sep + '..') + os.sep + "Input Hazirlayici" + os.sep + "file_index.json", 'r') as f:
    js = json.load(f)
player_line_num = js["PPN"]["line_num"]
model = None
if not os.path.exists("cs_model_test1.h5"):
    dim = 1  # GameFormat
    dim += player_line_num * 2
    model = Sequential()
    model.add(LSTM(300, batch_input_shape=(batch_size, timesteps, dim), consume_less="mem",
                   stateful=True))
    model.add(Dropout(0.02))
    #model.add(LSTM(100, consume_less="mem"))
    model.add(Dense(1, activation="sigmoid"))
    model.summary()

    model.compile(loss='binary_crossentropy',
                  optimizer="adam",
                  metrics=['accuracy'])
    model.save("cs_model_test1.h5")
turn = [0]
accuracy = [0.0, 0]
try:
    train(turn)
except Exception as ex:
    pass

print 'Finished training.'
score = model.evaluate(final_test, final_test_out, batch_size=batch_size, verbose=0)
print "\nTotal Accuracy"
print score[1]
print "\nFinished on turn:", turn[0]
print ""
print score

SR = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
for i in range(final_test_out.shape[0]):
    # t = final_test[i][0].tolist()
    # second_test = np.array([t[0]] + t[player_line_num+1:] + t[1:player_line_num+1])
    x = [[final_test[i][0]], [final_test[i][0]]]
    y = final_test_out[i]
    sonuc = model.predict(np.array(x))[0]
    print sonuc
    if sonuc[0] >= 0.5 and sonuc[0] < 0.55:
        SR[0][0] += 1
        if y[0] == 1:
            SR[0][1] += 1
    elif sonuc[0] >= 0.55 and sonuc[0] < 0.6:
        SR[1][0] += 1
        if y[0] == 1:
            SR[1][1] += 1
    elif sonuc[0] >= 0.6 and sonuc[0] < 0.65:
        SR[2][0] += 1
        if y[0] == 1:
            SR[2][1] += 1
    elif sonuc[0] >= 0.65 and sonuc[0] < 0.70:
        SR[3][0] += 1
        if y[0] == 1:
            SR[3][1] += 1
    elif sonuc[0] >= 0.70 and sonuc[0] < 0.75:
        SR[4][0] += 1
        if y[0] == 1:
            SR[4][1] += 1
    elif sonuc[0] >= 0.75 and sonuc[0] < 0.80:
        SR[5][0] += 1
        if y[0] == 1:
            SR[5][1] += 1
    elif sonuc[0] >= 0.80 and sonuc[0] < 0.85:
        SR[6][0] += 1
        if y[0] == 1:
            SR[6][1] += 1
    elif sonuc[0] >= 0.85 and sonuc[0] < 0.90:
        SR[7][0] += 1
        if y[0] == 1:
            SR[7][1] += 1
    elif sonuc[0] >= 0.90 and sonuc[0] < 0.95:
        SR[8][0] += 1
        if y[0] == 1:
            SR[8][1] += 1
    elif sonuc[0] >= 0.95 and sonuc[0] <= 1.0:
        SR[9][0] += 1
        if y[0] == 1:
            SR[9][1] += 1
prnt = ["50", "55", "60", "65", "70", "75", "80", "85", "90", "95", "100"]
i = 0
for sr in SR:
    if sr[0] == 0:
        sr[0] = 1
    print "for", prnt[i], '-', prnt[i + 1], "in", sr[0], "match, success is: ", float(sr[1]) * 100 / sr[0], "%"
    i += 1
