<template>
  <div id="app" class="container-fluid">
    <div id="header" class="container-fluid">
      <h1>シンデレラガールズ<wbr>台詞判定</h1>
    </div>
    <predict></predict>
  </div>
</template>

<script>
import Predict from './components/Predict'

export default {
  name: 'app',
  components: {
    Predict
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
