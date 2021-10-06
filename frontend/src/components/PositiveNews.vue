<template>
    <div class="stock_info" style="">
        <p style="font-size: 24px;">긍정 뉴스</p>
        <p style="color: blue;">Positive</p>
        <ul>
            <li :class="{'news_odd': i%2==1, 'news_even': i%2==0}" v-for="(item, i) in link" v-bind:key="item"><div class="info_title"></div><p>&nbsp; <a :href="item" target="_blank">{{ positiveNews[i] }}</a> &nbsp; </p></li>
        </ul>
    </div>
</template>

<script>
export default {   
    name: "PositiveNews",
    props:{
        positiveNews: Array,
        link: Array
    },
    data(){
        return{
        }
    },
    methods:{

    },
    watch:{
        positiveNews(){

        },
        link(){

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
.info_title ~p a{
    /* width : 40%; */
    text-overflow: ellipsis;
}

.stock_info{
    padding: 0;
    margin: 0;
    height: 100%;
    
    overflow-y:scroll;
}

.stock_info>ul{
    padding: 0;
    margin: 0;
    font-size: 1.0em;
    text-align:center;
    
}

.stock_info>ul>li:not(:last-child){
    margin: 0;
    
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

a { 
    text-decoration:none;
 } 

ul{
   list-style:none;
}

.news_odd{
    background-color: MediumSeaGreen;
}

.news_even{
    background-color:chartreuse
}

</style>