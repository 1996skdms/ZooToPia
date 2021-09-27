<template>
  <div id="app">
    <div id="nav">
      <router-link to="/"></router-link> 
    </div>
    <router-view />
  </div>
</template>

<script>

export default {
  name: "App",
  props:{
  },
  components:{
  }
}
</script>

<style>
#app {
  font-family: "Noto Sans KR", sans-serif;
  height: 100%;
  min-height: 100vh;
}
</style>
