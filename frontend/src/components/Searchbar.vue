<template>
    <div class="left-pad">
        <div class="wrapper">
            <div class="search">
            <div name="cse" id="searchbox_demo" class="searchform row" autocomplete="off">
                <div class="col-md-11">
                    <input type="text" placeholder="종목검색" class="searchbox form-control" v-model=searchWord v-on:keyup.enter="onOmit()"/>
                </div>
                <div class="col-md-1">
                    <button class="btn" @click="onOmit()">Search</button>
                </div>
                
            </div>
            </div>
        </div>
    </div>
</template>

<script>


export default {
    name: "Searchbar",
    data(){
        return{
            searchWord: "",
        }
    },
    methods:{
        onOmit(){
            console.log(this.searchWord)
            this.$emit("searchStock", this.searchWord)
        },
    },
}
</script>

<style>

.left-pad{
    position:absolute;
    width: 100%;
    padding-top:50px;
    padding-left: 100px;
}
</style>