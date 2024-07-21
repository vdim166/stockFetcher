import stockFetcher from "./stockFetcher"
import { computeData } from "./utils"
import supportResistanceFinder from "./supportResistanceFinder"

import { writeFile } from "fs/promises"

const SYMBOL = "SBER"
const NUM_CLUSTERS = 10

const figi = "BBG004730N88"
const tinkoffInterval = "CANDLE_INTERVAL_DAY"
const instrumentId = "e6123145-9665-43e0-8413-cd61b8aa9b13"

const run = async () => {
  const timeSeries = await stockFetcher.tinkoffFetchStockData({
    figi,
    interval: tinkoffInterval,
    instrumentId,
    fromDay: 1,
    toDay: 18,
    fromMonth: 1,
    toMonth: 7,
  })

  const { closingPrices, data } = computeData(timeSeries)

  const supportResistanceLevels =
    supportResistanceFinder.findSupportResistanceLevels(
      closingPrices,
      NUM_CLUSTERS
    )

  const outputData = {
    data: data,
    supportResistanceLevels: supportResistanceLevels,
    SYMBOL,
  }

  await writeFile("stockData.json", JSON.stringify(outputData, null, 2))
}

run()
