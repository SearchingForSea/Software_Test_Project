<template>
  <div id="app">
    <button @click="submit">发送</button>
  </div>
</template>

<script>

export default {
  name: 'App',
  components: {
  },
  methods: {
    submit() {
      this.$https.get('http://127.0.0.1:8000/api/show_res').then((response) => {
        console.log(response)
      }).catch((error) => {
        console.log(error)
      })
    }
  }
}
</script>

<style>
#app {
}
</style>
