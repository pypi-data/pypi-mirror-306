#!/usr/bin/env python3

import numpy as np
from diresa.models import build_diresa
from diresa.loss import mse_dist_loss, LatentCovLoss
from tensorflow.keras import backend as K
from diresa.callback import LossWeightAnnealing
from diresa.toolbox import cut_sub_model
from tensorflow.keras.models import load_model


def load_dataset():
    data_file = "docs/lorenz.csv"
    data = np.loadtxt(data_file, delimiter=",")
    train = data[:5000]
    val = data[5000:6000]
    id_train = np.argsort((np.random.random(train.shape[0])))
    id_val = np.argsort((np.random.random(val.shape[0])))
    train_twin = train[id_train]
    val_twin = val[id_val]
    return train, train_twin, val, val_twin


def test_diresa():
    train, train_twin, val, val_twin = load_dataset()

    # build the model
    diresa = build_diresa(input_shape=(3,), dense_units=(40, 20, 2))
    cov_weight = K.variable(0.)
    diresa.compile(loss=['MSE', LatentCovLoss(cov_weight), mse_dist_loss], loss_weights=[1., 1., 1.5])

    # train the model
    diresa.fit((train, train_twin), train,
               validation_data=((val, val_twin), val),
               epochs=5, batch_size=512, shuffle=True, verbose=2)

    # encoder submodel
    cut_sub_model(diresa, 'Encoder')

    # save and open model
    diresa.save('diresa.keras')
    load_model('diresa.keras')


def test_annealing_diresa():
    train, train_twin, val, val_twin = load_dataset()

    # build the model
    diresa = build_diresa(input_shape=(3,), dense_units=(40, 20, 2))
    cov_weight = K.variable(0.)
    diresa.compile(loss=['MSE', LatentCovLoss(cov_weight), mse_dist_loss], loss_weights=[1., 1., 1.5])

    # train the model
    callback = [LossWeightAnnealing(cov_weight, loss_name="val_Latent_loss", target_loss=0.0001, anneal_step=0.2,
                                    start_epoch=3)]
    diresa.fit((train, train_twin), train,
               validation_data=((val, val_twin), val),
               epochs=5, batch_size=512, shuffle=True, verbose=0, callbacks=callback)

    # decoder submodel
    cut_sub_model(diresa, 'Decoder')

    # save and open model
    diresa.save('diresa.keras')
    load_model('diresa.keras')


if __name__ == "__main__":
    test_diresa()
