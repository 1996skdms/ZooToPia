<template>
  <div class="row">
        <div class="col-md-3 row">
            <div class="col-md-1"></div>
            <div class="finance_summary col-md-4" v-text="labels[0]"></div>
            <div class="finance_summary col-md-5" style="text-align: right; float: left !important;">{{a}}</div>
            <div class="col-md-2"></div>
            <div class="col-md-1"></div>
            <div class="finance_summary col-md-4" v-text="labels[1]"></div>
            <div class="finance_summary col-md-5" style="text-align: right; float: left !important;" v-text="b"></div>
            <div class="col-md-2"></div>
        </div>
        <div class="col-md-3 row">
            <div class="col-md-1"></div>
            <div class="finance_summary col-md-5" v-text="labels[2]"></div>
            <div class="finance_summary col-md-5" style="text-align: right; float: left !important;" v-text="c"></div>
            <div class="col-md-1"></div>
            <div class="col-md-1"></div>
            <div class="finance_summary col-md-5" v-text="labels[3]"></div>
            <div class="finance_summary col-md-5" style="text-align: right; float: left !important;" v-text="d"></div>
            <div class="col-md-1"></div>
        </div>
        <div class="col-md-3 row">
            <div class="col-md-2"></div>
            <div class="finance_summary col-md-5" v-text="labels[4]"></div>
            <div class="finance_summary col-md-5" style="text-align: right; float: left !important;" v-text="e"></div>
            <div class="col-md-2"></div>
            <div class="finance_summary col-md-5" v-text="labels[5]"></div>
            <div class="finance_summary col-md-5" style="text-align: right; float: left !important;" v-text="f"></div>
        </div>
        <div class="col-md-3 row">
            <div class="col-md-3"></div>
            <div class="finance_summary col-md-4" v-text="labels[6]"></div>
            <div class="finance_summary col-md-5" style="text-align: right; float: left !important;" v-text="g"></div>
            <div class="col-md-3"></div>
            <div class="finance_summary col-md-4" v-text="labels[7]"></div>
            <div class="finance_summary col-md-5" style="text-align: right; float: left !important;" v-text="h"></div>
        </div>
  </div>
</template>

<script>
export default {
    name: "FinanceInfo",
    props: ["labels", "a", "b", "c", "d", "e", "f", "g", "h"],
    watch:{
    },
}
</script>

<style>

</style>