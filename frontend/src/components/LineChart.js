import { Line, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
    name: "LineChart",
    extends: Line,
    mixins: [reactiveProp],
    mounted () {
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
