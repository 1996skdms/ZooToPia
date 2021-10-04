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
                            beginAtZero: false
                        }
                    }]
            },
            responsive: true,
            maintainAspectRatio: false,
            outerHeight: 400,
        })
    },
    watch: {
        chartData: function() {
            this.renderChart(this.chartData, {
                scales: {
                    yAxes: [
                        {
                            ticks: {
                                beginAtZero: false
                            }
                        }]
                },
                responsive: true,
                maintainAspectRatio: false,
                outerHeight: 400,
            })
        }
    }
}
