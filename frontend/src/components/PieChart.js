
import { Doughnut } from "vue-chartjs"

export default {
  name: "PieChart",
  extends: Doughnut,
  props: ['bid', 'ask'],
  mounted() {
    this.renderPieChart()
  },
  watch: {
    bid: function () {
      console.log("watch: ", this.bid)
      this.chartData = [this.bid, this.ask]
      this.renderPieChart()
    }
  },
  data() {
    return {
      chartData: [this.bid, this.ask]  
    }
  },
  methods: {
    renderPieChart: function () {
      console.log("render change:", this.chartData)
      this.renderChart({
        labels: ["매수", "매도"],
        datasets: [
          {
            label: "Data",
            backgroundColor: [
              "rgba(235, 10, 10, 0.6)",
              "rgba(54, 162, 235, 0.6)",
            ],
            data: [this.chartData[0], this.chartData[1]]
          }
        ]
      },
      {
        borderWidth: "10px",
        hoverBackgroundColor: "red",
        hoverBorderWidth: "10px",
        responsive: true,
        maintainAspectRatio: false,
        scales: {
        },
      });
    }
  },

};
  
