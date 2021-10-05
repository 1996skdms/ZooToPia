<template>
    <div class="stock_info" style="">
        <p style="font-size: 24px;">부정 뉴스</p>
        <p style="color: red;">Negative</p>
        <ul>
            <li><div class="info_title">뉴스1</div>{{ negativeNews[0] }}</li>
            <li><div class="info_title">뉴스2</div>{{ negativeNews[1] }}</li>
            <li><div class="info_title">뉴스3</div>{{ negativeNews[2] }}</li>
            <li><div class="info_title">뉴스4</div>{{ negativeNews[3] }}</li>
        </ul>
    </div>
</template>

<script>
export default {   
    name: "NegativeNews",
    props:{
        negativeNews: Array
    },
    data(){
        return{
        }
    },
    methods:{

    },
    watch:{
        negativeNews(){

        }
    },
    computed:{
        
    }
}
</script>

<style>
.info_title{
    color: rgb(158, 152, 152);
    font-size: 0.6em !important;
    /* width: 100%; */
}

.stock_info>ul>li:not(:last-child){
    font-size: 1.5em;
    text-align:center;
    float:center;
    padding-bottom: 15px;
    border-bottom:rgb(107, 156, 179) 1px solid;
}
.stock_info>ul>li:not(:first-child){
    padding-top: 10px;
}
.stock_info>ul>li:not(last-child){
    font-size: 1.5em;
    text-align:center;
    float:center;
}


</style>