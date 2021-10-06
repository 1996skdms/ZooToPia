<template>
<div>
    <div v-if="isMidday">
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
                매도 <div style="font-size: 1.8em; ">{{ask}}%</div>
            </div>
            <div class="col-md-2"></div>
        </div>
    </div>
    <div v-else>
        장마감
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
    data(){
        return {
            day: this.$moment().day(),
            hour: this.$moment().hour(),
            minute: this.$moment().minute()
        }
    },
    computed:{
        isMidday: function(){
            if(this.day >= 1 && this.day <= 5 && 
                ((this.hour >= 9 && this.hour <= 14) || (this.hour == 15 && this.minute < 30))) return true;
            else return false;
        }
    }
}
</script>

<style>

</style>