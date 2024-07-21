import { ITinkoffResponse } from "./types/ICandleResponse"
import { IStock } from "./types/IStock"

export const computeData = (timeSeries: IStock) => {
  const data = Object.keys(timeSeries)
    .map((time) => ({
      date: time,
      ...timeSeries[time],
    }))
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())

  const closingPrices = data.map((item) => parseFloat(item["4. close"]))

  return { data, closingPrices }
}

export const convertToCorrectDay = (day: number) => {
  const dayString = day.toString()

  return dayString.length < 2 ? `${0}${dayString}` : dayString
}

export function transformData(apiResponse: ITinkoffResponse) {
  const result: IStock = {}

  apiResponse.candles.forEach((candle) => {
    const date = candle.time.split("T")[0]
    const openPrice = `${parseInt(candle.open.units)}.${
      candle.open.nano / 10000000
    }`
    const highPrice = `${parseInt(candle.high.units)}.${
      candle.high.nano / 10000000
    }`
    const lowPrice = `${parseInt(candle.low.units)}.${
      candle.low.nano / 10000000
    }`
    const closePrice = `${parseInt(candle.close.units)}.${
      candle.close.nano / 10000000
    }`
    const volume = candle.volume

    result[date] = {
      "1. open": openPrice,
      "2. high": highPrice,
      "3. low": lowPrice,
      "4. close": closePrice,
      "5. volume": volume,
    }
  })

  return result
}
