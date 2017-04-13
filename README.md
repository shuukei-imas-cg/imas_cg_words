# シンデレラガールズ台詞判定
Text classification for imas_cg words. use SVN(Confidence Weighted Learning)

「アイドルマスターシンデレラガールズ」(C)窪岡俊之 (C)BANDAI NAMCO Entertainment Inc. に登場する183人のアイドルの台詞を入力として183クラス分類を行う線形分類器を学習し、任意のテキストが入力されたときに「どのアイドルが発した台詞らしいか」を出力するサービスです。

本サービスは以下のURLで稼働しています(本リポジトリのものからいくらかアレンジが追加されています)。
本リポジトリのソースファイルにより、自分で学習データを用意することで、任意のタイトルの台詞判定サービスを自作することが可能です。

- http://www.shuukei.info/imas_cg_words/


## Requirement
動作確認は、CentOS 6.9, Python 2.7.11, Jubatus 1.0.2, MeCab 0.996, 最新のmecab-ipadic-NEologdで行っています。

また、添付のサンプルモデルファイルはJubatus 1.0.2専用です。他のバージョンではロードできません。

- Python (2.7以降)
- Jubatus
- MeCab
- mecab-ipadic-NEologd(強く推奨)


## サンプルファイルの構成

- localservice

    ローカルPCのコンソールで台詞判定を行う一番簡単なサンプルです。

- jubatus

    Jubatusの設定ファイル、ならびにサンプルモデルファイル(3人分)です。

- webapi

    外部に公開可能なWeb APIを構成するサンプルです(予定)

- frontend

    上記Web API用のフロントエンドです(予定)


## 利用手順
CentOS 6.9の場合のインストール手順を以下に示します。Ubuntuでも使用は可能なはずですが、その場合はJubatus及びmecab-ipadic-NEologdのインストール手順を参照して、Ubuntu用の手順に読み替えてください。

### localservice
1. Jubatusとそのクライアント、Pythonクライアントライブラリをインストールする
	- http://jubat.us/ja/quickstart.html
2. Mecabおよびmecab-ipadic-NEologdをインストールする。mecab-ipadic-NEologdのインストールが成功すると、インストール先のディレクトリが表示されるので、それをメモしておいてください。
	- https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md#例-動作に必要なライブラリのインストール
3. 以下の手順を実施する
~~~
git clone https://github.com/shuukei-imas-cg/imas_cg_words.git
cd imas_cg_words/jubatus
# mecab-ipadic-NEologdのインストール先によっては、serif.jsonの変更が必要になる場合があります
jubaclassifier -f serif.json -m model/sample.jubatus &
cd ..
cd localservice/
python classify.py
~~~
学習済みモデルファイルsample.jubatusには、3人のアイドル(喜多日菜子、棟方愛海、浅利七海)の台詞から学習した特徴のみが保存されています。

### webapi
準備中

### frontend
準備中


## Copyrights
- source: MIT License
- Pre-trained Model: All rights reserved.
