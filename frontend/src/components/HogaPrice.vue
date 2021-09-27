<template>
  <div>
        <ul class="hoga_title" style="float:right; text-align:right;">
            <li>
                <div class="hoga_info" style="text-align:center;">호가</div>
            </li>
            <li><div class="hoga_info">{{Price[9]}}</div></li>
            <li><div class="hoga_info">{{Price[8]}}</div></li>
            <li><div class="hoga_info">{{Price[7]}}</div></li>
            <li><div class="hoga_info">{{Price[6]}}</div></li>
            <li><div class="hoga_info">{{Price[5]}}</div></li>
            <li><div class="hoga_info">{{Price[4]}}</div></li>
            <li><div class="hoga_info">{{Price[3]}}</div></li>
            <li><div class="hoga_info">{{Price[2]}}</div></li>
            <li><div class="hoga_info">{{Price[1]}}</div></li>
            <li><div class="hoga_info">{{Price[0]}}</div></li>
        </ul>
  </div>
</template>

<script>
export default {
    name: "HogaPrice",
    props: ["Price"],
    methods:{

    },
    watch:{
        Price(){

        }
    },
}
</script>

<style>
</style>