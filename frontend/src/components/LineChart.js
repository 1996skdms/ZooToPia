import { Line, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
    name: "LineChart",
    extends: Line,
    mixins: [reactiveProp],
    mounted () {
    // this.chartData is created in the mixin.
    // If you want to pass options please create a local options object
        this.renderChart(this.chartData, {
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
        })
    },
    watch: {
        chartData: function() {
            
        }
    }
}
