<template>
    <div class="col-md-4 stock_info_s" style="">
        <ul>
            <li>
                <div v-if="isMidday" class="info_title_s">현재가</div>
                <div v-if="!isMidday" class="info_title_s">종가</div>
                &nbsp;{{stockToday.Close}}&nbsp;
            </li>
            <li><div class="info_title_s">시가</div>&nbsp;{{stockToday.Open}}&nbsp;</li>
            <li><div class="info_title_s">고가</div>&nbsp;{{stockToday.High}}&nbsp;</li>
            <li><div class="info_title_s">저가</div>&nbsp;{{stockToday.Low}}&nbsp;</li>
            <li><div class="info_title_s">거래량(주)</div>&nbsp;{{stockToday.Volume}}&nbsp;</li>
        </ul>
    </div>
</template>

<script>
export default {   
    name: "StockInfo",
    props: {
        stockToday: Object,
    },
    data(){
        return{
            day: this.$moment().day(),
            hour: this.$moment().hour(),
        }
    },
    methods:{

    },
    watch:{
        stockToday(){

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
.info_title_s{
    color: rgb(158, 152, 152);
    font-size: 0.6em !important;
}

.stock_info_s>ul>li:not(:last-child){
    font-size: 1.5em;
    text-align:center;
    float:center;
    padding-bottom: 15px;
    border-bottom:rgb(107, 156, 179) 1px solid;
}
.stock_info_s>ul>li:not(:first-child){
    padding-top: 10px;
}
.stock_info_s>ul>li:not(last-child){
    font-size: 1.5em;
    text-align:center;
    float:center;
}


</style>