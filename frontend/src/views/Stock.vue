<template>
    <div>
        <div class="row">
            <Sidebar></Sidebar>
        </div>
        <div class="row">
            <SearchBar v-on:searchStock="searchStock"></SearchBar>
        </div>
        <div v-if="searchWord==''">
            
        </div>
        <div v-else>
            <div class="row outer_box">
                <div class="row">
                    <div class="stock_remark_title_s col-md-8">주가</div>
                    <div class="stock_remark col-md-7">of {{now}} AM</div>
                    <div class="stock_remark col-md-3" style="padding-left:50px;">
                        <button class="duration_button" @click="setDuration(0)">3년</button>
                        <button class="duration_button" @click="setDuration(1)">1년</button>
                        <button class="duration_button" @click="setDuration(2)">3개월</button>
                        <button class="duration_button" @click="setDuration(3)">1달</button>
                        <button class="duration_button" @click="setDuration(4)">2주</button>
                    </div>
                </div>
                <div class="row stock_chart">
                    <LineChart :height="400" class="col-md-8" :chart-data="stock_graph"></LineChart>
                    <StockInfo v-bind:stockToday="stockToday"></StockInfo>
                </div>

            </div>
            
            <div class="row outer_box" style="margin-top:50px; !important;">
                <div class="row hoga_stage">
                <div class="row col-md-3">
                    <HogaChart :ask="pieChartAsk" :bid="pieChartBid"></HogaChart>
                </div>
                <Hoga class="col-md-9" v-bind:askPrice="askPrice" :bidPrice="bidPrice" 
                :askVolume="askVolume" :bidVolume="bidVolume"></Hoga>
                </div>
            </div>

            <div class="row outer_box" style="margin-top:50px; !important;">
                <div class="row finance_info">
                    기업정보
                </div>
                <div class="row stock_remark col-md-7">of {{searchWord}}</div>
                <div> &nbsp;</div>

                <FinanceInfo class="finance_info col-md-12" :labels="labels" :a="finance_summary.linkedSales"
                                :b="finance_summary.separateSales"  :c="finance_summary.revenue"
                                :d="finance_summary.asset"  :e="finance_summary.netIncome" 
                                :f="finance_summary.odds"  :g="finance_summary.liability"
                                :h="finance_summary.name"></FinanceInfo>

                <div class="row bar_chart">
                    <div class="col-md-3">
                        <div class="col-md-1"></div>
                        <BarChart class="col-md-9" :height="250" :financeData="finance.linked_sales" :label="labels[0]"></BarChart>  
                        <div class="col-md-1"></div>
                    </div>
                    <div class="col-md-3">
                        <div class="col-md-1"></div>
                        <BarChart class="col-md-9" :height="250" :financeData="finance.separate_sales"  :label="labels[1]"></BarChart> 
                        <div class="col-md-1"></div>
                    </div>
                    <div class="col-md-3">
                        <div class="col-md-1"></div>
                        <BarChart class="col-md-9" :height="250" :financeData="finance.revenue" :label="labels[2]"></BarChart>
                        <div class="col-md-1"></div>
                    </div>
                    <div class="col-md-3">
                        <div class="col-md-1"></div>
                        <BarChart class="col-md-9" :height="250" :financeData="finance.asset"  :label="labels[3]"></BarChart>
                        <div class="col-md-1"></div>
                    </div>
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
import LineChart from "../components/LineChart.js"
import StockInfo from "../components/StockInfo.vue"
import HogaChart from "../components/HogaChart.vue"
import Hoga from "../components/Hoga.vue"
import BarChart from "../components/BarChart.js"
import FinanceInfo from "../components/FinanceInfo.vue"

export default {
    name: "Stock",
    components:{
        Sidebar,
        SearchBar,
        LineChart,
        StockInfo,
        HogaChart,
        Hoga,
        BarChart,
        FinanceInfo,
    },
    data() {
        return {
            socket: null,
            status: "",
            hogaInterval: null,
            intervalCheck: "",

            searchWord: "",
            stockProfile: {},

            duration: 3,            // 0: 3년, 1: 1년, 2: 3개월, 3: 1개월, 4: 2주

            stockToday: {},
            
            now: this.$moment(new Date()).format("DD MMM YYYY HH:mm:ss"),

            askPrice: [],
            askVolume: [],
            bidPrice: [],
            bidVolume: [],

            finance: [],
            labels: ['매출액(연결)', '매출액(별도)', '영업이익(연결)', '자산',
                    '당기순이익', '배당률', '부채', '기업명'],
            finance_summary: {},

            stock_graph: {},
            predict_stock_graph: {},
    
            pieChartAsk: 0,
            pieChartBid: 0,
            //[ this.rateOfBidVolume, this.rateOfAskVolume],

        }
    },
    methods: {
        async getStockProfile(searchWord){
            const res = await stock.getStockProfile(searchWord)
            return res.data;
        },
        async searchStock(searchWord){
            this.predict_stock_graph = {}

            let data = await this.getStockProfile(searchWord)
            this.searchWord = data.NAME

            this.stockProfile = data

            // this.socketConnect()
            
            this.stockGraph(this.stockProfile.symbol)

            this.getToday(this.stockProfile.symbol)

            await this.removeHoga()
            await this.registerHoga(this.stockProfile.symbol)
            this.getHoga(this.stockProfile.symbol)

            await this.financeInfo(data.NAME)
        },
        async stockGraph(symbol){
            let dur = 30
            if(this.duration == 0) dur = 365*3
            else if(this.duration == 1) dur = 365
            else if(this.duration == 2) dur = 91
            else if(this.duration == 3) dur = 30
            else if(this.duration == 4) dur = 14

            let res = await stock.getStockGraph(symbol, dur)
            if(this.predict_stock_graph.date == undefined) {
                await this.stockPredict(this.stockProfile.symbol)
            }

            this.stock_graph = {
                labels: res.data.date.concat(this.predict_stock_graph.date),
                datasets: [
                {
                    data: res.data.close.concat(this.predict_stock_graph.close),
                    label: this.stockProfile.NAME,
                    borderColor: "#3e95cd",
                    fill: false
                },
                ]
            }
        },
        async stockPredict(symbol){
            let res = await stock.getstockPredict(symbol)
            console.log(res)

            this.predict_stock_graph.close = res.data.close
            this.predict_stock_graph.date = res.data.date
        },
        async registerHoga(symbol){
            this.intervalCheck = symbol
            stock.registerHoga(symbol)
        },
        async getHoga(symbol){
            this.hogaInterval = setInterval(() => {
                if(this.intervalCheck == symbol) this.getRealTimeHogaMethod(symbol)
                else clearInterval(this.hogaInterval)
            }, 1500)
        },
        async getRealTimeHogaMethod(symbol){
            let res = await stock.getRealTimeHoga(symbol)
            console.log(res.data)

            this.bidPrice = []
            this.bidVolume = []
            this.askPrice = []
            this.askVolume = []

            res.data.forEach((e) => {
                this.askPrice[e.ordering - 1] = e.ask_price.substring(1, e.length)
                this.askVolume[e.ordering - 1] = e.ask_volume
                this.bidPrice[e.ordering - 1] = e.bid_price.substring(1, e.length)
                this.bidVolume[e.ordering - 1] = e.bid_volume
            })
        },
        async removeHoga(){
            if(this.hogaInterval != null) clearInterval(this.hogaInterval)
            this.intervalCheck = false
            await stock.removeHoga(this.stockProfile.symbol)
        },
        async getToday(symbol){
            let res = await stock.getStockToday(symbol)
            
            this.stockToday = res.data
            console.log("종목 금일 정보: ", this.stockToday)
        },
        async financeInfo(searchWord){
            let res = await stock.getFinancialInfo(searchWord)

            this.finance = {}
            this.finance = res.data

            let lastYear = Number(this.$moment(new Date()).format("YYYY")) - 1
            this.finance_summary.linkedSales = this.convertUnit(this.finance.linked_sales[lastYear])
            this.finance_summary.separateSales = this.convertUnit(this.finance.separate_sales[lastYear])
            this.finance_summary.revenue = this.convertUnit(this.finance.revenue[lastYear])
            this.finance_summary.asset = this.convertUnit(this.finance.asset[lastYear])
            this.finance_summary.netIncome = this.convertUnit(this.finance.net_income[lastYear])
            this.finance_summary.liability = this.convertUnit(this.finance.liability[lastYear])
            this.finance_summary.odds = this.finance.odds + '%'
            this.finance_summary.odds_cash = this.finance.odds_cash + '원'
            this.finance_summary.name = searchWord

            console.log("Finance Summary: ", this.finance_summary)
            
        },
        setDuration(dur){
            this.duration = dur
            this.stockGraph(this.stockProfile.symbol)
        },
        convertUnit(cash){
            if(cash == 'NaN' || cash == undefined) return '-'

            let jo = ""
            let uk = ""
            if(cash >= 1000000000000){
                jo = Math.floor(cash / 1000000000000) + '조'
            }
            uk = (Math.round((cash % 1000000000000) / 10000000) /10 )+ '억'

            return jo + ' ' + uk
        }
    },
    mounted(){
        setInterval(() => {
            this.now = this.$moment(new Date()).format("DD MMM YYYY HH:mm:ss")
        }, 1000)

        // this.searchStock("삼성전자") // 테스트

    },
    watch:{
        rateOfBidVolume(){
            this.pieChartAsk = this.rateOfAskVolume
            this.pieChartBid = this.rateOfBidVolume
        }
    },
    computed:{
        rateOfAskVolume(){
            let sum = 0
            let sum2 = 0
            this.askVolume.forEach(e => {
                sum += Math.abs(e)
            })

            this.bidVolume.forEach(e => {
                sum2 += Math.abs(e)
            })
            let rate = sum / (sum + sum2)
            if(isNaN(rate)) return 0

            rate = Math.round(rate * 100)
            return rate
           
        },
        rateOfBidVolume(){
            return 100 - this.rateOfAskVolume;
        }
    }
}
</script>

<style>
.left-pad{
    position: absolute;
    width: 100%;
    top:0px;
    left: 0px;
}

.outer_box{
    margin-top: 130px;
    background-color: rgb(245, 250, 248);
    border-radius: 0 15% 15% 0;
    border: white 1px solid;
    padding-top: 20px;
    padding-bottom: 20px;
}

.stock_chart{
    position:relative;
    /* top: 130px; */
    left: 100px;
}

.stock_info_s{
    padding-top:30px;
    padding-right:100px;
}

.stock_info_s>ul{
    list-style-type: none;
    margin-left: -40px;
    margin-right:60px;
    color:rgb(19, 60, 61);
}

.stock_remark_title_s{
    position:relative;
    /* top:120px; */
    padding-left:120px;
    font-size:1.4em;
}

.stock_remark{
    position:relative;
    /* top:120px; */
    padding-left:120px;
    font-size:0.5em;
}


.duration_button:hover {
  background-color: #52a5e9; /* Green */
  color: white;
}

.duration_button {
  transition-duration: 0.4s;
  background-color: white;
  color: black;
  border: 2px solid #bcc9c7b7;
  border-radius: 4px;
}

.hoga_stage{
    position: relative;
    padding-left: 120px;
    /* top: 180px; */
}

.sell_amount{
    text-align: center;
    float: center;
    font-size: 0.8em;
    margin-top: 0px;
    line-height: 250%;
}

.finance_info{
    position: relative;
    padding-left: 120px;
    font-size:1.4em;
}

.finance_summary{
    position: relative;
    text-align: left;
    font-size: 0.6em;
    padding-bottom: 10px;
    margin-bottom: 10px;
    border-bottom: #bcc9c7b7 1px solid;
}

.bar_chart{
    position: relative;
    padding-left: 120px;
    padding-top: 40px;
}

</style>