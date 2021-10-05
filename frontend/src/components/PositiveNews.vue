<template>
    <div class="stock_info" style="">
        <p style="font-size: 24px;">긍정 뉴스</p>
        <p style="color: blue;">Positive</p>
        <ul>
            <li><div class="info_title">뉴스1</div>&nbsp;{{ positiveNews[0] }}&nbsp;</li>
            <li><div class="info_title">뉴스2</div>&nbsp;{{ positiveNews[1] }}&nbsp;</li>
            <li><div class="info_title">뉴스3</div>&nbsp;{{ positiveNews[2] }}&nbsp;</li>
            <li><div class="info_title">뉴스4</div>&nbsp;{{ positiveNews[3] }}&nbsp;</li>
        </ul>
    </div>
</template>

<script>
export default {   
    name: "PositiveNews",
    props:{
        positiveNews: Array
    },
    data(){
        return{
        }
    },
    methods:{

    },
    watch:{
        positiveNews(){

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
}

.stock_info{
    padding: 0;
    margin: 0;
}

.stock_info>ul{
    padding: 0;
    margin: 0;
}

.stock_info>ul>li:not(:last-child){
    margin: 0;
    font-size: 1.5em;
    text-align:center;
    float:center;
    padding-bottom: 15px;
    border-bottom:rgb(107, 156, 179) 1px solid;
}
.stock_info>ul>li:not(:first-child){
    padding-top: 10px;
}

/* .stock_info>ul>li:not(last-child){
    font-size: 1.5em;
    text-align:center;
    float:center;
} */


</style>