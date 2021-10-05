<template>
<div>
  <wordcloud
      :data="defaultWords"
      nameKey="name"
      valueKey="value"
      :color="myColors"
      :showTooltip="true"
      :wordClick="wordClickHandler">
  </wordcloud>
</div>

</template>

<script>
import wordcloud from "vue-wordcloud"

export default {
  name: "WordCloud",
  props:{
    data: Array,
    myColors: Array,
  },
  components:{
    wordcloud,
  },
  methods:{
    wordClickHandler(name, value, vm) {
      this.$emit(console.log('wordClickHandler', name, value, vm));
    }
  },
  data(){
    return{
        
    }
  },
}
</script>

<style>

</style>