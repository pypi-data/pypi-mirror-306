import tensorflow as tf
from toolbox import covariance
import tensorflow_probability as tfp
import numpy as np


data = np.array([[1., 4, 2, -2], [5, 6, 24, 10], [15, 1, 5, 0], [7, 3, 8, -5], [9, 4, 7, 8], [9, 4, 7, 8]])

print((covariance(tf.constant(data, dtype=tf.float32))))
print(tfp.stats.covariance(data))
