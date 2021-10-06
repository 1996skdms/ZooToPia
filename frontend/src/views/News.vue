<template>
    <div>
        <div class="row">
            <Sidebar></Sidebar>
        </div>
        <div class="row">
            <SearchBar v-on:searchStock="searchStock"></SearchBar>
        </div>
        <div v-if="isLoading ? false : true" class="lb-wrap2">
            <div class="lb-image2" >
                <img style="width: 30%" src="../Spinner.gif">
            </div>
            <div class="lb-text2">
                <br>
                <h2 style="font-size: 30px;">분석 중 입니다. 잠시만 기다려주세요!</h2>
            </div>
        </div>
        <div v-if="isLoading" class="row count">
            <div class="count_box">
                <p>검색된 기사 개수</p>
                <p>{{ totalNews }}</p>
            </div>
            <div class="count_box">
                <p>분석된 단어 개수</p>
                <p>{{ vocab_size }}</p>
            </div>
            <div class="count_box">
                <p>긍정 기사 개수</p>
                <p>{{ pos_count }}</p>
            </div>
            <div class="count_box">
                <p>부정 기사 개수</p>
                <p>{{ neg_count }}</p>
            </div>
        </div>
        <div v-if="isLoading" class="row middle">
            <div class="row">
                <div class="word_cloud col-md-8">Word Cloud</div>
                <div class="word_cloud_remark col-md-7">of {{now}} AM</div>
            </div>
            <div class="row word_cloud_chart">
                <div class="word_cloud_position col-md-8">
                    <word-cloud :data="defaultWords" :myColors="myColors"></word-cloud>
                </div>
                <div class="chart_score_positon col-md-4">
                    <div class="pie_chart_box">
                        <div class="pie_chart">
                            <Pie :data="chartData" :options="chartOptions"></Pie>
                        </div>
                    </div>
                    <div class="score_box">
                        <div class="score">Score</div>
                        <div class="grade">{{ score }}점</div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="isLoading" class="row PnN_news">
            <div class="row news">
                <div class="news_list col-md-6">
                    <PositiveNews :positiveNews="positiveTitle" :link="positiveNews"></PositiveNews>
                </div>
                <div class="news_list col-md-6">
                    <NegativeNews :negativeNews="negativeTitle" :link="negativeNews"></NegativeNews>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
/* eslint-disable */

import Sidebar from "../components/Sidebar.vue"
import SearchBar from "../components/Searchbar.vue"
import stock from "../api/stock"
import WordCloud from "vue-wordcloud"
import Pie from "../components/Pie.js"
import PositiveNews from "../components/PositiveNews.vue"
import NegativeNews from "../components/NegativeNews.vue"
import news from "../api/news"

export default {
    name: "News",
    components:{
        Sidebar,
        SearchBar,
        WordCloud,
        Pie,
        PositiveNews,
        NegativeNews
    },
    data(){
        return{
            isLoading: false,
            searchWord: "주식",

            myColors: ['#1f77b4', '#629fc9', '#94bedb', '#c9e0ef'],
            defaultWords: [{
                "name": "고양이",
                "value": 26
                },
                {
                "name": "생선",
                "value": 19
                },
                {
                "name": "물건",
                "value": 18
                },
                {
                "name": "look",
                "value": 16
                },
                {
                "name": "two",
                "value": 15
                },
                {
                "name": "fun",
                "value": 9
                },
                {
                "name": "know",
                "value": 9
                },
                {
                "name": "good",
                "value": 9
                },
                {
                "name": "play",
                "value": 6
                }
            ],

            now: this.$moment(new Date()).format("DD MMM YYYY HH:mm:ss"),

            totalNews: 60,
            score: 0,
            vocab_size: 0,
            pos_count: 0,
            neg_count: 0,
            positiveTitle: [],
            negativeTitle: [],
            chartOptions: {
                hoverBorderWidth: 20
            },
            chartData: {
                hoverBackgroundColor: "red",
                hoverBorderWidth: 10,
                labels: ["중립", "긍정", "부정"],
                datasets: [
                    {
                        label: "Data One",
                        backgroundColor: ["#41B883", "#00D8FF", "#E46651"],
                        data: [10,10,10]
                    }
                ]
            },

            positiveNews: ["https://www.naver.com/", "https://www.google.co.kr/", "https://www.acmicpc.net/", "https://programmers.co.kr/"],
            negativeNews: ["https://github.com/", "https://jasoseol.com/", "https://edu.ssafy.com/", "https://www.notion.so/"]
            
        }
    },
    methods:{
        async getSearchNewsInfo(searchWord){
            this.isLoading = false
            const res = await news.getSearchNewsInfo(searchWord)
            console.log("getSearchNewsInfo res >>>>> ", res.data)
            return res.data;
        },
        async getStockProfile(searchWord){
            const res = await stock.getStockProfile(searchWord)
            return res.data;
        },
        async searchStock(searchWord){
            let data = await this.getSearchNewsInfo(searchWord)
            this.totalNews = data.total_count
            // this.score = data.score_mean.toFixed(2)
            this.score =  (this.totalNews - 0.5*( data.pos_count+ data.neg_count)-data.neg_count / this.totalNews * 100).toFixed(2)
            this.vocab_size = data.vocab_size
            this.positiveNews =  data.pos_link
            this.positiveTitle = data.pos_title
            this.negativeNews = data.neg_link
            this.negativeTitle = data.neg_title
            this.positive_ratio = data.positive_ratio
            this.negaitive_ratio = data.negaitive_ratio
            this.pos_count = data.pos_count
            this.neg_count = data.neg_count
            this.defaultWords = data.word_cloud
            this.chartData.datasets[0].data[2] = data.negaitive_ratio
            this.chartData.datasets[0].data[1] = data.positive_ratio
            this.chartData.datasets[0].data[0] = Math.abs(data.negaitive_ratio - data.positive_ratio).toFixed(2)

            this.isLoading = true
        },
        // wordClickHandler(name, value, vm) {
        //     this.$emit(console.log('wordClickHandler', name, value, vm));
        // }
    },
    watch:{
    },
    mounted(){
        setInterval(() => {
            this.now = this.$moment(new Date()).format("DD MMM YYYY HH:mm:ss")
        }, 1000),

        this.searchStock('코스피')
    }
}
</script>

<style>
.lb-wrap2 {
  width: 100%;
  position: relative;
  text-align: center;
}
.lb-wrap2 img {
  width: 100%;
  margin-top: 10%;
  text-align: center;
}
.lb-text2 {
  width: 100%;
  border-radius: 10px;
  /* text-align: center; */
  color:rgb(32, 64, 168);
  position: absolute;
  /* transform: translate(-50%, -50%); */
}
.count{
    width: 90%;
    position: relative;
    top: 150px;
    left: 120px;
}

.count_box{
    display: inline;
    width: 24%;
    border: 1px solid;
    text-align: center;
    margin: 0 5px;
    background-color: rgb(245, 250, 248);
    /* border-radius: 0 15% 15% 0; */
    border: white 1px solid;
}

.middle{
    margin-top: 180px;
    background-color: rgb(245, 250, 248);
    border-radius: 0 15% 15% 0;
    border: white 1px solid;
    padding-top: 20px;
    padding-bottom: 20px;
}
.Loading{
    margin-top: 180px;
    text-align: center;
}
.word_cloud{
    position:relative;
    /* top:180px; */
    padding-left:120px;
    font-size:1.4em;
}

.word_cloud_remark{
    position:relative;
    /* top:180px; */
    padding-left:120px;
    font-size:0.5em;
}

.word_cloud_chart{
    width: 90%;
    position:relative;
    /* top:180px; */
    left:120px;   
}

.word_cloud_position{
    border: 1px solid;
}

.pie_chart_box{
    position: relative;
    height: 60%;
    border: 1px solid;
}

.pie_chart{
    margin: 0;
    font-family: "Avenir", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
}

.score_box{
    position: relative;
    height: 40%;
    border: 1px solid;
    text-align: center;
    display: flex;
    flex-direction: column;
    display: block;
}

.score{
    margin: 0;
    height: 50%;
    vertical-align: middle;
    /* padding: 5%; */
}

.grade{
    margin: 0;
    height: 50%;
    vertical-align: middle;
    /* padding: 5%; */
}

.PnN_news{
    margin-top: 40px;
    background-color: rgb(245, 250, 248);
    border-radius: 0 15% 15% 0;
    /* border: white 1px solid; */
    padding-top: 20px;
    padding-bottom: 20px;
}

.news{
    width: 90%;
    position:relative;
    /* top:210px; */
    left:120px;
}

.news_list{
    display: inline-block;
    width : 49%;
    height: 400px;
    border: 1px solid;
    margin: 0 5px;
    background-color: white;
}


</style>
