# -*- coding:utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import json
import logging

import falcon
import jubatus
from config import host, port, name, httpdhost, httpdport
from jubatus.common import Datum

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='log/predict.log', level=logging.INFO)


def predict(words):
    """
    台詞を入力として候補をスコア降順に返す
    :type words: unicode
    :rtype: list[dict]
    """
    client = jubatus.Classifier(host, port, name)
    datum = Datum({'serif': words})
    res = client.classify([datum])
    sorted_res = sorted(res[0], key=lambda x: -x.score)
    del client

    results = [{"name:": resp.label, "score": resp.score} for resp in sorted_res if resp.score != 0]
    return results


def _add_headers(resp):
    """httpヘッダを追加する"""
    resp.set_header('Access-Control-Allow-Origin', '*')
    resp.set_header('Access-Control-Allow-Headers', '*')
    resp.set_header('Access-Control-Allow-Methods', 'GET')
    resp.set_header('Content-Type', 'application/json;charset=utf-8')


class PredictSerif(object):
    """WebAPIのハンドラ"""

    def on_get(self, req, resp, words):
        result = predict(words)
        json_out = json.dumps(result, indent=4, ensure_ascii=False)
        _add_headers(resp)
        resp.body = json_out
        resp.status = falcon.HTTP_200
        logging.info("predict {0} {1}".format(req.remote_addr, words.decode('utf-8')))


# Add route
api = falcon.API()
api.add_route('/imas_cg-words/v1/predict/{words}', PredictSerif())


def main():
    logging.info("Server Started by Development Environment.")
    from wsgiref import simple_server
    httpd = simple_server.make_server(httpdhost, httpdport, api)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
