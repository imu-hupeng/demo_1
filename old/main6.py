import tensorflow as tf
import numpy as np
import matplotlib.pyplot  as plt


def add_layer(input, in_size, out_size, activation_function = None):
    with tf.name_scope("layer"):
        # 随机变量
        with tf.name_scope("weight"):
            Weight = tf.Variable(tf.random_normal([in_size, out_size]), name="W")
        with tf.name_scope("bases"):
            biases = tf.Variable(tf.zeros([1, out_size]) + 0.1, name="b")
        with tf.name_scope("Wx_plus_b"):
            Wx_plus_b = tf.add(tf.matmul(input, Weight) , biases)
        if activation_function is None:
            outputs = Wx_plus_b
        else:
            outputs = activation_function(Wx_plus_b)
        return outputs

# 确定输入的数据
x_data = np.linspace(-1, 1, 300)[:, np.newaxis]
noise = np.random.normal(0, 0.05, x_data.shape)
y_data = np.square(x_data) - 0.5 + noise
with tf.name_scope("inputs"):
    xs = tf.placeholder(tf.float32, [None, 1], name="x_input")
    ys = tf.placeholder(tf.float32, [None, 1], name="y_input")

# 输入层
l1 = add_layer(xs, 1, 10, tf.nn.relu)
prediction = add_layer(l1, 10, 1, None)

with tf.name_scope("loss"):
    loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys-prediction), reduction_indices=[1]))
with tf.name_scope("train"):
    train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

init = tf.initialize_all_variables()



with tf.Session() as sess:
    writer = tf.train.SummaryWriter("logs/", sess.graph)
    sess.run(init)

    for i in range(10000):
        sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
        if i % 50 == 0:
            print(sess.run(loss, feed_dict={xs: x_data, ys: y_data}))
