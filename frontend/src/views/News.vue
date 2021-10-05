<template>
    <div>
        <div class="row">
            <Sidebar></Sidebar>
        </div>
        <div class="row">
            <SearchBar v-on:searchStock="searchStock"></SearchBar>
        </div>    
        <div class="row count">
            <div class="count_box">
                <p>검색된 기사 개수</p>
                <p>{{ totalNews }}</p>
            </div>
            <div class="count_box">
                <p>분석된 단어 개수</p>
                <p>{{ analyzeWord }}</p>
            </div>
            <div class="count_box">
                <p>긍정 기사 개수</p>
                <p>{{ posVolume }}</p>
            </div>
            <div class="count_box">
                <p>부정 기사 개수</p>
                <p>{{ negVolume }}</p>
            </div>
        </div>
        <div class="row middle">
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
                        <div class="grade">{{ grade }}점</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row PnN_news">
            <div class="row news">
                <div class="news_list col-md-6">
                    <PositiveNews :positiveNews="positiveNews"></PositiveNews>
                </div>
                <div class="news_list col-md-6">
                    <NegativeNews :negativeNews="negativeNews"></NegativeNews>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import Sidebar from "../components/Sidebar.vue"
import SearchBar from "../components/Searchbar.vue"
import stock from "../api/stock"
import WordCloud from "vue-wordcloud"
import Pie from "../components/Pie.js"
import PositiveNews from "../components/PositiveNews.vue"
import NegativeNews from "../components/NegativeNews.vue"

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

            searchWord: "삼성전자",

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
            analyzeWord: 16,
            posVolume: 43,
            negVolume: 64,

            chartOptions: {
                hoverBorderWidth: 20
            },
            chartData: {
                hoverBackgroundColor: "red",
                hoverBorderWidth: 10,
                labels: ["Green", "Red", "Blue"],
                datasets: [
                    {
                        label: "Data One",
                        backgroundColor: ["#41B883", "#E46651", "#00D8FF"],
                        data: [1, 10, 5]
                    }
                ]
            },

            grade: 80,

            positiveNews: ["https://www.naver.com/", "https://www.google.co.kr/", "https://www.acmicpc.net/", "https://programmers.co.kr/"],
            negativeNews: ["https://github.com/", "https://jasoseol.com/", "https://edu.ssafy.com/", "https://www.notion.so/"]
        }
    },
    methods:{
        async getStockProfile(searchWord){
            const res = await stock.getStockProfile(searchWord)
            return res.data;
        },
        async searchStock(searchWord){
            let data = await this.getStockProfile(searchWord)
            this.searchWord = data.NAME
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
        }, 1000)
    }
}
</script>

<style>
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
    display: inline;
    width : 49%;
    border: 1px solid;
    margin: 0 5px;
    background-color: white;
}


</style>
