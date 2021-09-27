<template>
  <div>
        <ul class="hoga_title">
            <li>
                <div class="hoga_info under_line">{{askBid}}</div>
            </li>
            <li><div class="hoga_info">10</div></li>
            <li><div class="hoga_info">9</div></li>
            <li><div class="hoga_info">8</div></li>
            <li><div class="hoga_info">7</div></li>
            <li><div class="hoga_info">6</div></li>
            <li><div class="hoga_info">5</div></li>
            <li><div class="hoga_info">4</div></li>
            <li><div class="hoga_info">3</div></li>
            <li><div class="hoga_info">2</div></li>
            <li><div class="hoga_info">1</div></li>
        </ul>
  </div>
</template>

<script>
export default {
    name: "HogaStandard",
    props: ["askBid"],
    methods:{

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
    border-bottom: rgb(113, 170, 172) 1px solid;
}

.hoga_info{
    color: rgb(158, 152, 152);
    font-size: 1em;
    padding-bottom: 5px;
}
</style>