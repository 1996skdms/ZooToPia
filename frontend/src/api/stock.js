/* eslint-disable */
import _axios from "./default"
export default {
    getStockProfile(stockName) {
        return _axios({
            url: `/stock/symbol`,
            method: 'get',
            params: {
                name: stockName
            },
        })
    },
    getStockToday(symbol) {
        return _axios({
            url: `/stock/today`,
            method: 'get',
            params: {
                symbol: symbol
            },
        })
    },
    getFinancialInfo(stockName) {
        console.log(stockName)
        return _axios({
            url: `/stock/financial_info`,
            method: 'get',
            params: {
                name: stockName,
            },
        })
    },
    getStockGraph(symbol, duration) {
        return _axios({
            url: `/stock/last`,
            method: 'get',
            params: {
                symbol: symbol,
                duration: duration,
            },
        })
    },
    getstockPredict(symbol) {
        return _axios({
            url: `/stock/predict`,
            method: 'get',
            params: {
                symbol: symbol
            },
        })
    },
    getRealTimeHoga(symbol) {
        return _axios({
            url: `/stock/realtime_hoga`,
            method: 'get',
            params: {
                symbol: symbol,
            },
        })
    },
    registerHoga(symbol) {
        return _axios({
            url: `/stock/register_hoga`,
            method: 'post',
            params: {
                symbol: symbol,
            },
        })
    },
    removeHoga(symbol) {
        return _axios({
            url: `/stock/remove_hoga`,
            method: 'delete',
            params: {
                symbol: symbol,
            },
        })
    },
}