# coding: utf-8

import sys
from collections import Counter

import numpy as np
from imp import reload
import tensorflow.contrib.keras as kr
import os
if sys.version_info[0] > 2:
    is_py3 = True
else:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    is_py3 = False


def native_word(word, encoding='utf-8'):
    """如果在python2下面使用python3训练的模型，可考虑调用此函数转化一下字符编码"""
    if not is_py3:
        return word.encode(encoding)
    else:
        return word


def native_content(content):
    if not is_py3:
        return content.decode('utf-8')
    else:
        return content


def open_file(filename, mode='r'):
    """
    常用文件操作，可在python2和python3间切换.
    mode: 'r' or 'w' for read or write
    """
    if is_py3:
        return open(filename, mode, encoding='utf-8', errors='ignore')
    else:
        return open(filename, mode)


def read_file(filename):
    """读取文件数据"""
    contents, labels = [], []
    with open_file(filename) as f:
        for line in f:
            try:
                label, content = line.strip().split('\t')
                if content:
                    contents.append(content)
                    labels.append(label)
            except:
                pass
    return contents, labels


def build_vocab(train_dir, vocab_dir, vocab_size=160):
    """根据训练集构建词汇表，存储"""
    data_train, _ = read_file(train_dir)

    all_data = []
    for content in data_train:
        tmp_list = content.split(",")
        for cont in tmp_list:
            # if cont not in all_data:
            all_data.append(cont)


    counter = Counter(all_data)
    count_pairs = counter.most_common(vocab_size - 1)
    words, _ = list(zip(*count_pairs))
    # 添加一个 <PAD> 来将所有文本pad为同一长度
    words = ['<PAD>'] + list(words)
    open_file(vocab_dir, mode='w').write('\n'.join(words) + '\n')


def read_vocab(vocab_dir):
    """读取词汇表"""
    # words = open_file(vocab_dir).read().strip().split('\n')
    with open_file(vocab_dir) as fp:
        # 如果是py2 则每个值都转化为unicode
        words = [native_content(_.strip()) for _ in fp.readlines()]
    word_to_id = dict(zip(words, range(len(words))))
    return words, word_to_id


def read_category():
    """读取分类目录，固定"""
    categories = ['丙肝', '乙肝', '前列腺炎', '盆腔炎', '肠胃炎', '肾炎', '肾结石', '肾绞痛', '胆囊炎', '胆结石','胰腺炎','阑尾炎']

    categories = [native_content(x) for x in categories]

    cat_to_id = dict(zip(categories, range(len(categories))))

    return categories, cat_to_id


def to_words(content, words):
    """将id表示的内容转换为文字"""
    return ''.join(words[x] for x in content)


def process_file(filename, word_to_id, cat_to_id, max_length=6):
    """将文件转换为id表示"""
    contents, labels = read_file(filename)
    for i, val in enumerate(contents):
        contents[i] = val.split(",")
    data_id, label_id = [], []
    for i in range(len(contents)):
        data_id.append([word_to_id[x] for x in contents[i] if x in word_to_id])
        label_id.append(cat_to_id[labels[i]])

    # 使用keras提供的pad_sequences来将文本pad为固定长度
    x_pad = kr.preprocessing.sequence.pad_sequences(data_id, max_length)
    y_pad = kr.utils.to_categorical(label_id, num_classes=len(cat_to_id))  # 将标签转换为one-hot表示

    return x_pad, y_pad


def  batch_iter(x, y, batch_size=64):
    """生成批次数据"""
    data_len = len(x)
    num_batch = int((data_len - 1) / batch_size) + 1

    indices = np.random.permutation(np.arange(data_len))
    x_shuffle = x[indices]
    y_shuffle = y[indices]

    for i in range(num_batch):
        start_id = i * batch_size
        end_id = min((i + 1) * batch_size, data_len)
        yield x_shuffle[start_id:end_id], y_shuffle[start_id:end_id]



def feed_data(x_batch, y_batch, keep_prob):
    feed_dict = {
        "input_x": x_batch,
        "input_y": y_batch,
        "keep_prob": keep_prob
    }
    return feed_dict


if __name__ == '__main__':
    vocab_dir = 'cnews/desc-vocab.txt'
    train_dir = os.path.join('cnews', 'desc-train.txt')
    build_vocab(train_dir, vocab_dir, vocab_size=160)
    categories, cat_to_id = read_category()
    words, word_to_id = read_vocab(vocab_dir)

    x_train, y_train = process_file(train_dir, word_to_id, cat_to_id, 6)
    print (x_train)
    print (y_train)

    batch_train = batch_iter(x_train, y_train, 64)
    for x_batch, y_batch in batch_train:
        feed_dict = feed_data(x_batch, y_batch, 0.5)

        print(feed_dict)

    print(batch_train)
