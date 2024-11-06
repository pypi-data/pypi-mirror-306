#!/usr/bin/env python3
"""
DIRESA helper functions

:Author:  Geert De Paepe
:Email:   geert.de.paepe@vub.be
:License: MIT License
"""

import tensorflow as tf
from tensorflow.keras.models import Model


def covariance(x):
    mean_x = tf.expand_dims(tf.reduce_mean(x, axis=0), 0)
    mx = tf.matmul(tf.transpose(mean_x), mean_x)
    vx = tf.matmul(tf.transpose(x), x)/tf.cast(tf.shape(x)[0], tf.float32)
    cov_xx = vx - mx
    return cov_xx


def cut_sub_model(model, sub_model_name):
    """
    Cuts a sub-model out of a keras model 
    Limitations: does not work for a sub-model of a sub-model
    
    :param model: keras model
    :param sub_model_name: name of the sub-model
    :return: submodel
    """
    sub_model_nbr = None
    sub_model_config = None

    for nbr, layer in enumerate(model.get_config()['layers']):
        if layer['name'] == sub_model_name:
            sub_model_config = layer['config']
            sub_model_nbr = nbr

    if sub_model_config is None:
        print(sub_model_name, " not found in model")
        exit(1)

    sub_model = Model.from_config(sub_model_config)
    weights = [layer.get_weights() for layer in model.layers[sub_model_nbr].layers[1:]]

    for layer, weight in zip(sub_model.layers[1:], weights):
        layer.set_weights(weight)

    return sub_model
