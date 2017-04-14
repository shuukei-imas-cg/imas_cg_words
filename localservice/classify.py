# -*- coding:utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import jubatus
from config import host, port, name
from jubatus.common import Datum


def predict():
    while True:
        client = jubatus.Classifier(host, port, name)
        words = raw_input().decode("utf-8")
        datum = Datum({'serif': words})
        res = client.classify([datum])
        predicted_dic = sorted(res[0], key=lambda x: -x.score)
        for result in predicted_dic:
            print("label:{0} score:{1}".format(result.label, result.score))


if __name__ == '__main__':
    predict()
