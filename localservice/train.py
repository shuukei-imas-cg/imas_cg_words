# -*- coding:utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import csv
import random
import sys

import jubatus
from config import host, port, name
from jubatus.common import Datum


def train(client, csv_filename):
    fr = open(csv_filename, 'r')
    reader = csv.reader(fr)
    header = next(reader)  # ヘッダーを読み飛ばす

    train_data = []
    for line in reader:
        train_data.append((line[0], Datum({'serif': line[1]})))
    print("train data length={0}".format(str(len(train_data))))

    # training data must be shuffled on online learning!
    random.shuffle(train_data)

    for data in train_data:
        client.train([data])


def main():
    if len(sys.argv) != 2:
        print("Usage: python " + sys.argv[0] + " input_csv_file")
        exit()
    # filename = "data/sample.csv"
    filename = sys.argv[1]

    # connect to the jubatus
    client = jubatus.Classifier(host, port, name)

    train(client, filename)
    client.save(name)


if __name__ == '__main__':
    main()
