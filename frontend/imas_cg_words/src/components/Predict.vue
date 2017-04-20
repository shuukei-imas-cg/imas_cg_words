<template>
  <div class="predict container-fluid">
    <div class="wordsinput container">
      <textarea id="words" v-model="words" v-on:keyup.ctrl.enter="hantei_btn" placeholder="台詞を入力してください"></textarea>
      <br>
      <button id="predict" v-on:click="hantei_btn" type="button" class="btn btn-success btn-block" v-bind:disabled="btn_disable">判定</button>
    </div>

    <div v-if="error" class="container">
      <p class="bg-danger">APIサーバの反応がありません。サービスはメンテナンス中です。</p>
    </div>

    <div class="input_words container" v-if="input_words != ''">
      <p>Words: {{ input_words }}</p>
    </div>

    <div class="idol-results container">
      <table id="results" class="table table-striped">
      <thead v-if="predict_val != ''">
        <tr>
          <th>Rank</th><th>Name</th><th>Score</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ret in predict_results">
          <td class="number">{{ ret.number }}</td><td class="name">{{ ret.name }}</td><td class="score">{{ ret.score }}</td>
        </tr>
      </tbody>
      </table>
    </div>

  </div>
</template>

<script>
import WordsNormalization from '../modules/Words.js'

export default {
  name: 'predict',
  data () {
    return {
      words: '',
      input_words: '',
      predict_val: '',
      error: false
    }
  },
  methods: {
    hantei_btn: function () {
      this.predict()
    },
    predict: function (event) {
      if (this.words === '') {
        return
      }
      var param = 'predict/' + encodeURIComponent(WordsNormalization(this.words))
      this.$http.get(param).then(response => {
        // success callback
        if (response.body.length === 0) {
          this.predict_val = ''
          this.input_words = WordsNormalization(this.words)
          return
        }
        this.predict_val = response.body
        this.input_words = WordsNormalization(this.words)
        this.error = false
      }, response => {
        // error callback
        this.error = true
        this.predict_val = ''
      })
    }
  },
  computed: {
    predict_results: function () {
      if (this.predict_val === '') {
        return ''
      }
      var ret = []
      for (var i = 0; i < this.predict_val.length; i++) {
        ret[i] = {'number': i + 1, 'name': this.predict_val[i]['name'], 'score': this.predict_val[i]['score']}
      }
      this.selected_idol = this.predict_val[0]['name']
      return ret
    },
    btn_disable: function () {
      return this.words === ''
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.predict {
  font-family: Meiryo,sans-serif;
}
div.wordsinput {
  margin-top: 20px;
  margin-bottom: 20px;
}
.input_words {
  margin-top: 10px;
}
textarea {
  height: 5em;
  width: 100%;
}
td.name, td.score {
  text-align: left;
}
</style>
