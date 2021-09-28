<template>
  <div>
        <ul class="hoga_title">
            <li>
                <div class="hoga_info under_line">{{askBid}}</div>
            </li>

            <li v-for="(e, i) in hoga" :key="i">
                <div class="hoga_info" v-text="e">
                </div>
            </li>
        </ul>
  </div>
</template>

<script>
export default {
    name: "HogaStandard",
    props: ["askBid"],
    data(){
        return {
            hoga: []
        }
    },
    created() {
        console.log(this.askBid)
        if(this.askBid == '매수'){
            console.log("매수")
            for(let i=0; i<10; i++) {
                this.hoga[i] = i+1;
            }
        }
        else{
            console.log("매도")
            for(let i=0; i<10; i++) {
                this.hoga[i] = 10 - i;
            }
        }
       
    }
}
</script>

<style>
.hoga_title{
    list-style-type: none;
    float: center;
    text-align: center;
}

.under_line{
    padding-bottom: 10px;
    border-bottom: rgb(72, 99, 121) 1px solid;
}

.hoga_info{
    color: rgb(121, 114, 114);
    font-size: 1em;
    padding-bottom: 5px;
}
</style>