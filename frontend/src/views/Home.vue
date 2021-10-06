<template>
    <div>
        <div class="row">
            <Sidebar></Sidebar>
        </div>
        <div class="lb-wrap">
            <div class="lb-text">
                <h1 style="padding-left:10px; font-size: 100px;">WELCOME</h1>
                <br>
                <h2 style="font-size: 70px;">STOCK INVESTMENT UTOPIA</h2>
            </div>
            <div class="lb-button" >
                <button @click=moveToNews() >주투피아 시작하기</button>
            </div>
            <div class="lb-image">
                <img style="width: 100%" src="../business-ga781e90a3_1920.jpg">
            </div>
        </div>
        <br>
        <br>
        <div class="row">
            <div style="text-align:center; width:100%" class="col col-md-8">
                <h2 class="featurette-heading" >주투피아 <span class="text-muted">  : 주식 투자 유토피아</span></h2>
                <br>
                <p class="lead">성공적인 주식 투자를 위한 데이터 분석 플랫폼<br></p>
            </div>  
            <br>
        </div>
        <br><br><br>
        <hr class = "hrstyle">

        <div class="row featurette">
            <div class="col-img col-md-4">
                <svg class="bd-placeholder-img bd-placeholder-img-lg featurette-image img-fluid mx-auto" width="500" height="500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Placeholder: 500x500" preserveAspectRatio="xMidYMid slice" focusable="false"><title>Placeholder</title><rect width="100%" height="100%" fill="#eee"/><text x="50%" y="50%" fill="#aaa" dy=".3em">500x500</text></svg>
            </div>
            <div class="col col-md-8">
                <h2 class="featurette-heading">1. 뉴스기사 분석 서비스 <span class="text-muted"> + Word Cloud</span></h2>
                <p class="lead"> &nbsp;투자자에게 가장 중요한 것은 무엇일까요? 첫째는 정보, 둘째는 정확성입니다. <br>
                        뉴스 데이터 분석 시스템은 실시간으로 가장 정확한 뉴스 정보를 신속히 제공하여 투자를 위한 분석 시간을 단축시켜줍니다. <br>
                        또한, 자연어 감정 분석을 통해 시각적으로 보다 쉽게 데이터를 이해할 수 있도록 돕습니다.</p>
            </div>  
        </div>
        <hr class = "hrstyle">

        <div class="row featurette">
            <div class="col-md-8">
                <h2 class="featurette-heading">2. 주식 종목 예측 <span class="text-muted">  + Dart Info</span></h2>
                <p class="lead"> &nbsp;그래도 투자가 망설여지시나요? 뉴스 분석만으로는 부족하다고 느껴지시나요? <br>
                        증권사와 연계된 주식 종목 실시간 거래와 기업 분석 데이터를 통해 기업 정보를 얻고 복합 데이터 기반 미래 주가 예측 시스템의 도움을 받아 보다 안정적으로 미래를 위한 투자에 임해보세요!</p>
            </div>
            <div class="col-md-4">
                <img @click="moveToStock" style="cursor:pointer;" src="../stock_view.jpg" class="bd-placeholder-img bd-placeholder-img-lg featurette-image img-fluid mx-auto" width="500" height="500"/>
            </div>
        </div>
        <hr class = "hrstyle">
        <footer>
            <p style="float:right; margin-right:20px" ><a href="#">Back to top ▲</a></p>
            <p style="margin-left:5%" >&copy; 2021.09 – 2021.10 주투피아</p>
        </footer>
    </div>
</template>
<script>
/* eslint-disable */
import Sidebar from "../components/Sidebar.vue"
import _axios from "../api/default"

export default {
    name: "Home",
    components:{
        Sidebar,
    },
    data(){
        return{
            
        }
    },
    methods:{
        moveToNews(){
            console.log("잘 눌렀니?")
            this.$router.push({name: "News"}).catch(() => {})
        },
        moveToStock(){
            console.log("잘 눌렀니?")
            this.$router.push({name: "Stock"}).catch(() => {})
        },
    },
    mounted(){
        setInterval(() => {
            this.now = this.$moment(new Date()).format("DD MMM YYYY HH:mm:ss")
        }, 1000)
    }
}
</script>
<style scoped>
button{
  background:#0ee0afc0;
  color:#fff;
  border:none;
  position:relative;
  height:60px;
  font-size:1.6em;
  padding:0 2em;
  cursor:pointer;
  transition:800ms ease all;
  outline:none;
  font-weight: bold;
}
button:hover{
  background:#fff;
  color:#1AAB8A;
}
button:before,button:after{
  content:'';
  position:absolute;
  top:0;
  right:0;
  height:2px;
  width:0;
  background: #1AAB8A;
  transition:400ms ease all;
}
button:after{
  right:inherit;
  top:inherit;
  left:0;
  bottom:0;
}
button:hover:before,button:hover:after{
  width:100%;
  transition:800ms ease all;
}
.lb-wrap {
  width: 100%;
  position: relative;
}
.lb-wrap img {
  width: 100%;
}
.lb-text {
  width: 100%;
  padding: 10px 20px;
  border-radius: 10px;
  text-align: center;
  color:white;
  position: absolute;
  top: 30%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.lb-button {
  width: 100%;
  padding: 10px 20px;
  border-radius: 10px;
  text-align: center;
  color:white;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.featurette{
  position: relative;
  left: 5%;
}

hr.hrstyle{
    margin-left: 5%;
    border: 2px;
    height: 1px;
    background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
}
</style>
