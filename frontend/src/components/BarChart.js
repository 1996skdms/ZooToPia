import { Bar } from 'vue-chartjs'

export default {
    name: "BarChart",
    extends: Bar,
    props:["financeData", "label"],
    mounted () {
        this.renderBarChart()
    },
    watch: {
        financeData: function() {
            this.renderBarChart()
        }
    },
    methods: {
        renderBarChart() {
            if (this.financeData == undefined) return
            
            let year = Number(this.$moment(new Date()).format("YYYY")) - 4

            let divide = 1000000
            let unit = "억"
            for (let i = 0; i < 4; i++){
                if (this.financeData[year + i] >= 1000000000000) {
                    divide = 10000000000
                    unit = "조"
                } 
            }

            
            let barData = {
                labels: [String(year), String(year+1), String(year+2), String(year+3)],
                datasets: [
                {
                    label: this.label + ": 단위(" + unit + ")",
                    data: [
                        Math.round(this.financeData[year] / divide) / 100,
                        Math.round(this.financeData[year+1] / divide) / 100,
                        Math.round(this.financeData[year+2] / divide) / 100,
                        Math.round(this.financeData[year+3] / divide) / 100,
                    ],
                    backgroundColor: [
                        "rgba(54, 162, 235, 0.6)",
                        "rgba(54, 162, 235, 0.6)",
                        "rgba(54, 162, 235, 0.6)",
                        "rgba(54, 162, 235, 1)",
                    ]
                }, 
                ]
            }
            
            this.renderChart(barData, {
                scales: {
                    yAxes: [
                        {
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                },
                responsive: true,
                maintainAspectRatio: false,
                deep: true
            })
        },
    }
}