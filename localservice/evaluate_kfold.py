# -*- coding:utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import sys

import sklearn.metrics
from jubakit.classifier import Classifier, Schema, Dataset, Config
from jubakit.loader.csv import CSVLoader
from sklearn.cross_validation import StratifiedKFold

loader = CSVLoader(sys.argv[1])
schema = Schema({
    'Name': Schema.LABEL,
    'Serif': Schema.STRING,
})
dataset = Dataset(loader, schema).shuffle()

cfg = Config(
    method='CW',
    parameter={
        'regularization_weight': 1.0
    },
    converter={
        'string_rules': [
            {'key': 'Serif', 'type': 'mecab', 'sample_weight': 'bin', 'global_weight': 'bin'},
        ],
        'string_types': {
            "mecab": {
                "method": "dynamic",
                "path": "libmecab_splitter.so",
                "function": "create",
                "arg": "-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd",
                "ngram": "1",
                "base": "false",
                "include_features": "*",
                "exclude_features": ""
            }
        }
    }
)
classifier = Classifier.run(cfg)

true_labels = []
predicted_labels = []

for train_idx, test_idx in StratifiedKFold(list(dataset.get_labels()), n_folds=10):
    classifier.clear()
    (train_ds, test_ds) = (dataset[train_idx], dataset[test_idx])

    for (idx, label) in classifier.train(train_ds):
        pass

    for (idx, label, result) in classifier.classify(test_ds):
        pred_label = result[0][0]
        true_labels.append(label)
        predicted_labels.append(pred_label)

classifier.stop()

print(sklearn.metrics.classification_report(true_labels, predicted_labels))
