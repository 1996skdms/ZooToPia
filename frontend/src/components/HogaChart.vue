<template>
<div>
    <div class="row">
        <div class="col-md-1"></div>
        <pie-chart class="col-md-10" :height="250" :ask="ask" :bid="bid"></pie-chart>
        <div class="col-md-1"></div>
    </div>
    
    <div class="row">
        <div class="col-md-2"></div>
        <div class="col-md-4 sell_amount">
            매수 <div style="font-size: 1.8em;">{{bid}}%</div>
        </div>
        <div class="col-md-4 sell_amount">
            매도 <div style="font-size: 1.8em;">{{ask}}%</div>
        </div>
        <div class="col-md-2"></div>
    </div>
</div>

</template>

<script>
import PieChart from "../components/PieChart.js"

export default {
    name: "HogaChart",
    props: {
        ask: Number,
        bid: Number,
    },
    components:{
        PieChart,
    },
    methods:{

    },
}
</script>

<style>

</style>