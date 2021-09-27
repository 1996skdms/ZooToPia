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
            <div class="row">
                <div class="stock_remark_title col-md-8">주가</div>
                <div class="stock_remark col-md-7">of {{now}} AM</div>
                <div class="stock_remark col-md-3" style="padding-left:50px;">
                    <button class="duration_button" @click="setDuration(0)">1년</button>
                    <button class="duration_button" @click="setDuration(1)">3개월</button>
                    <button class="duration_button" @click="setDuration(2)">1달</button>
                    <button class="duration_button" @click="setDuration(3)">2주</button>
                </div>
            </div>
            <div class="row stock_chart">
                <LineChart :height="400" class="col-md-8" :chart-data="datacollection"></LineChart>
                <StockInfo v-bind:stockToday="stockToday"></StockInfo>
            </div>
            <div class="row hoga_stage">
                <div class="row col-md-3">
                    <HogaChart :ask="pieChartAsk" :bid="pieChartBid"></HogaChart>
                </div>
                <Hoga class="col-md-9" v-bind:askPrice="askPrice" :bidPrice="bidPrice" 
                :askVolume="askVolume" :bidVolume="bidVolume"></Hoga>
            </div>
            <div class="row finance_info">
                재무정보
            </div>
            <div class="row stock_remark col-md-7" style="top:240px;">of {{searchWord}}</div>
            <div> &nbsp;</div>
            <div class="row finance_info col-md-12">
                <div class="col-md-3">
                    <div class="finance_summary">매출액(연결)</div>
                    <div class="finance_summary">매출액(별도)</div>
                </div>
                <div class="col-md-3">
                    <div class="finance_summary">영업이익</div>
                    <div class="finance_summary">자산</div>
                </div>
                <div class="col-md-3">
                    <div class="finance_summary">당기순이익</div>
                    <div class="finance_summary">뭐할까</div>
                </div>
                <div class="col-md-3">
                    <div class="finance_summary">설립일</div>
                    <div class="finance_summary">주소</div>
                </div>
                
            </div>
            <div class="row bar_chart">
                <BarChart class="col-md-2" :height="250" :financeData="finance.linked_sales" :label="labels[0]"></BarChart>          <!--  :barData="finance" -->
                <div class="col-md-1"></div>
                <BarChart class="col-md-2" :height="250" :financeData="finance.separate_sales"  :label="labels[1]"></BarChart>
                <div class="col-md-1"></div>
                <BarChart class="col-md-2" :height="250" :financeData="finance.revenue"  :label="labels[2]"></BarChart>
                <div class="col-md-1"></div>
                <BarChart class="col-md-2" :height="250" :financeData="finance.asset"  :label="labels[3]"></BarChart>
            </div>
        </div>
        
    </div>
</template>

<script>
import Sidebar from "../components/Sidebar.vue"
import SearchBar from "../components/Searchbar.vue"
import stock from "../api/stock"
import LineChart from "../components/LineChart.js"
import StockInfo from "../components/StockInfo.vue"
import HogaChart from "../components/HogaChart.vue"
import Hoga from "../components/Hoga.vue"
import BarChart from "../components/BarChart.js"

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
    },
    data() {
        return {
            socket: null,
            status: "",

            searchWord: "",
            stockProfile: [],

            duration: 1,            // 0: 1년, 1: 3개월, 2: 1개월, 3: 2주

            stockToday: {},
            
            now: this.$moment(new Date()).format("DD MMM YYYY HH:mm:ss"),

            askPrice: [],
            askVolume: [],
            bidPrice: [],
            bidVolume: [],

            finance: [],
            labels: ['매출액(연결)', '매출액(별도)', '영업이익(연결)', '자산'],

            
            datacollection: {
                labels: ["week 1", "week 2", "week 3", "week 4", "week 5", "week 6", "week 7", "week 8", "week 9", "week 10"],
                datasets: [
                {
                    data: [86, 114, 106, 106, 107, 111, 133, 221, 783, 2478],
                    label: "Africa",
                    borderColor: "#3e95cd",
                    fill: false
                },
                {
                    data: [282, 350, 411, 502, 635, 809, 947, 1402, 3700, 1267],
                    label: "Asia",
                    borderColor: "#8e5ea2",
                    fill: false
                },
                ]
            },
    
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
            this.searchWord = searchWord

            let data = await this.getStockProfile(searchWord)
            let lastIdx = this.stockProfile.length
            this.stockProfile.push(data)

            this.socketConnect(lastIdx)

            await this.financeInfo(searchWord)
        },
        socketConnect(idx){
            console.log(this.stockProfile[idx].symbol)
            this.socket = new WebSocket("ws://localhost:8080/kiwoom/hoga/" + this.stockProfile[idx].symbol)
            this.socket.onopen = () => {
                this.status = "connected";
                let cnt = 0
                this.socket.onmessage = ({data}) => {
                    cnt = 1 - cnt
                    if(cnt % 2 != 0) this.getToday(this.stockProfile[idx].symbol)
                    // console.log(data)
                    // data = {
                    //     price: ["+77300", "+77400", "+77500", "+77600", "+77300", "+77400", "+77500", "+77600", "+77500", "+77600"],
                    //     volume: [468435,8643,6843,1580, 468435,8643,6843,158, 6843,158]
                    //     }
                    
                    data = JSON.parse(data)
                    // data = {
                    //     price: ["-77300", "-77400", "-77500", "-77600", "-77300", "-77400", "-77500", "-77600", "-77500", "-77600"],
                    //     volume: [468435,8643,6843,1580, 468435,8643,6843,158, 6843,158]
                    //     }
                    if(data.updown == "bid"){                    
                        this.bidPrice = []
                        this.bidVolume = []

                        for(let i=data.price.length - 1; i>=0; i--){
                            this.bidPrice[this.bidPrice.length] = data.price[i].substring(1,data.price[i].length)
                        }
                        for(let i=data.volume.length - 1; i>=0; i--){
                            this.bidVolume[this.bidVolume.length] = data.volume[i];
                        }
                    }
                    else if(data.updown == "ask"){
                        this.askPrice = []
                        this.askVolume = []

                        data.price.forEach(e => {
                            this.askPrice[this.askPrice.length] = e.substring(1,e.length)
                        });
                        data.volume.forEach(e => {
                            this.askVolume[this.askVolume.length] = e
                        });
                    }
                }
            }
        },
        async getToday(symbol){
            let res = await stock.getStockToday(symbol)
            
            this.stockToday = res.data
            console.log(this.stockToday)
        },
        async financeInfo(searchWord){
            let res = await stock.getFinancialInfo(searchWord)

            this.finance = {}
            this.finance = res.data

            console.log(this.finance)
            
        },
        setDuration(dur){
            this.duration = dur
        }
    },
    mounted(){
        setInterval(() => {
            this.now = this.$moment(new Date()).format("DD MMM YYYY HH:mm:ss")
        }, 1000)
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
            if(isNaN(rate)) return 49

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

.stock_chart{
    position:relative;
    top: 130px;
    left: 100px;
}

.stock_info{
    padding-top:30px;
    padding-right:100px;
}

.stock_info>ul{
    list-style-type: none;
    margin-left: -40px;
    margin-right:60px;
    color:rgb(29, 83, 85);
}

.stock_remark_title{
    position:relative;
    top:120px;
    padding-left:120px;
    font-size:1.4em;
}

.stock_remark{
    position:relative;
    top:120px;
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
    top: 180px;
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
    top: 240px;
    font-size:1.4em;
}

.finance_summary{
    position: relative;
    text-align: left;
    font-size: 0.7em;
}

.bar_chart{
    position: relative;
    padding-left: 120px;
    padding-top: 280px;
}

</style>