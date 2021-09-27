<template>
  <div>
        <ul class="hoga_title" style="float:left; text-align:left;">
            <li>
                <div class="hoga_info row" style="text-align:center; float:center;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;잔량</div>
            </li>
            <li><div class="hoga_info">{{Volume[9]}}</div></li>
            <li><div class="hoga_info">{{Volume[8]}}</div></li>
            <li><div class="hoga_info">{{Volume[7]}}</div></li>
            <li><div class="hoga_info">{{Volume[6]}}</div></li>
            <li><div class="hoga_info">{{Volume[5]}}</div></li>
            <li><div class="hoga_info">{{Volume[4]}}</div></li>
            <li><div class="hoga_info">{{Volume[3]}}</div></li>
            <li><div class="hoga_info">{{Volume[2]}}</div></li>
            <li><div class="hoga_info">{{Volume[1]}}</div></li>
            <li><div class="hoga_info">{{Volume[0]}}</div></li>
        </ul>
  </div>
</template>

<script>
export default {
    name: "HogaVolume",
    props: {
        Volume: Array,
    },
    data(){
        return{
        }
    },
    methods:{

    },
    watch:{
        Volume(){

        }
    },
}
</script>

<style>

</style>