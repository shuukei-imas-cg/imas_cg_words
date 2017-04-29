# シンデレラガールズ台詞判定
Text classification for imas_cg words. use SVN(Confidence Weighted Learning)

「アイドルマスターシンデレラガールズ」(C)窪岡俊之 (C)BANDAI NAMCO Entertainment Inc. に登場する183人のアイドルの台詞を入力として183クラス分類を行う線形分類器を学習し、任意のテキストが入力されたときに「どのアイドルが発した台詞らしいか」を出力するサービスです。

本サービスは以下のURLで稼働しています(本リポジトリのものからいくらかアレンジが追加されています)。
本リポジトリのソースファイルにより、自分で学習データを用意することで、任意のタイトルの台詞判定サービスを自作することが可能です。

- http://www.shuukei.info/imas_cg_words/

本リポジトリの内容の解説記事を書きました。
- http://qiita.com/shuukei-imas-cg/items/ea501e62970b309ceea4


## Requirement
動作確認は、CentOS 6.9, Python 2.7.11, Jubatus 1.0.2, MeCab 0.996, 最新のmecab-ipadic-NEologdで行っています。

また、添付のサンプルモデルファイルはJubatus 1.0.3および1.0.2用です。他のバージョンでは動作の保証はありません。

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

    外部に公開可能なWeb APIを構成するサンプルです

- frontend

    上記Web API用のフロントエンドです


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
jubaclassifier -f serif.json -m model/sample.1.0.2.jubatus &
cd ..
cd localservice/
python classify.py
~~~

学習済みモデルファイルsample.jubatusには、3人のアイドル(喜多日菜子、棟方愛海、浅利七海)の台詞から学習した特徴のみが保存されています。また、mecab-ipadic-NEologdのインストール先が/usr/local/lib/mecab/dic/mecab-ipadic-neologdに固定されています。
mecab-ipadic-NEologdのインストール先が異なる環境で実行する場合は、シンボリックリンクを張るか、[jubakit](https://github.com/jubatus/jubakit) 0.4.3以降に同梱のjubamodelを使用してモデル内に埋まっている設定を書き換えてください。


### webapi
WebアプリケーションフレームワークとしてFalcon、WSGIサーバーとしてGunicornを使用します。

1. あらかじめjubaclassifierの起動まで行っておく(localserviceの手順を参考)
2. Falcon, Gunicornのインストール
3. (Python組み込みのsimple_serverを使用して)ローカルホストで起動する
~~~
# Falcon, Gunicornをインストールする
pip install cython gunicorn
pip install --no-binary :all: falcon
# localhostでwebapiサーバを起動
cd webapi/
python server.py
# クエリ
curl http://localhost:8080/imas_cg-words/v1/predict/妄想
[
    {
        "score": 1.2635555267333984,
        "name:": "喜多日菜子"
    },
    {
        "score": -0.9001807570457458,
        "name:": "棟方愛海"
    },
    {
        "score": -1.0048713684082031,
        "name:": "浅利七海"
    }
]
~~~
curlでクエリを投げて上記のように表示されれば正常に動作しています。

外部からもアクセス可能なWeb APIとして公開する場合、simple_serverでは力不足ですので、以下のようにGunicornを用います。Gunicornから起動する場合、config.pyで設定したIPアドレスとポート番号は無視されることに注意します。
~~~
gunicorn -b (IPアドレス):(ポート番号) server:api &
# ワーカ数やログファイルを指定する場合
gunicorn -w 4 -b (IPアドレス):(ポート番号) --access-logfile log/access.log --error-logfile log/error.log server:api &
~~~

server.pyのjson.dumpsのindent=4は可読性のために設定してあります。本番では削除しても良いでしょう。

### frontend
Vue.js 2.0を用いたSPA(Single Page Application)です。事前にnode.jsをインストールしておく必要があります。
~~~
cd frontend/imas_cg_words/

# 必要パッケージのインストール。node_modules/ ディレクトリ以下にインストールされる(時間がかかります)
npm install
# ローカルサーバで起動
npm run dev
~~~
Vue.jsのwebpackボイラープレートを使用しています。npm run devを実行すると、ブラウザが起動し、http://localhost:8080でページが開きます。

frontend/imas_cg_words/src/main.jsの、Vue.http.options.rootの値を、自分で起動したWebAPIのURIに書き換えてください。TEXTAREAに適当なテキストを入力して判定ボタンを押し、結果が表示されれば成功です。

#### ビルドとデプロイ
~~~
npm run build
~~~
frontend/imas_cg_words/dist/ 以下にビルドされたhtml, js, cssなどのファイルが生成されますので、適当なWebサーバに配置してください。index.htmlをローカルでブラウザから読み込んでも動作しません。


## Copyrights
- source: MIT License
- Pre-trained Model: All rights reserved.

## Author
[@shuukei_imas_cg](https://twitter.com/shuukei_imas_cg)
