# coding: utf-8

from __future__ import print_function

import os
import tensorflow as tf
import tensorflow.contrib.keras as kr

from rnn_model import TRNNConfig, TextRNN
from data.cnews_loader import read_category, read_vocab

# try:
#     bool(type(unicode))
# except NameError:
#     unicode = str

base_dir = 'data/cnews'
vocab_dir = os.path.join(base_dir, 'desc-vocab.txt')

save_dir = 'checkpoints/textrnn'
save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径


class RnnModel:
    def __init__(self):
        self.config = TRNNConfig()
        self.categories, self.cat_to_id = read_category()
        self.words, self.word_to_id = read_vocab(vocab_dir)
        self.config.vocab_size = len(self.words)
        self.model = TextRNN(self.config)

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型

    def predict(self, message):
        # 支持不论在python2还是python3下训练的模型都可以在2或者3的环境下运行
        content = message
        data = [self.word_to_id[x] for x in content if x in self.word_to_id]

        feed_dict = {
            self.model.input_x: kr.preprocessing.sequence.pad_sequences([data], self.config.seq_length),
            self.model.keep_prob: 1.0
        }

        y_pred_cls = self.session.run(self.model.y_pred_cls, feed_dict=feed_dict)
        return self.categories[y_pred_cls[0]]


if __name__ == '__main__':
    rnn_model = RnnModel()
    test_demo = [
                 '急性,患者,HCV,感染,抗病毒,病毒', #丙肝
                 '胰液,手术,胰酶,结石,酗酒', # 胆结石
                 '压痛,患者,下腹,穿孔,腹痛,黏膜'#阑尾炎
                 ]
    for i in test_demo:
        print(rnn_model.predict(i))