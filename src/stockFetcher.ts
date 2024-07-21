import axios, { AxiosResponse } from "axios"
import config from "config"
import { convertToCorrectDay, transformData } from "./utils"
import { ITinkoffResponse } from "./types/ICandleResponse"

type tinkoffFetchStockData = {
  figi: string
  interval: string
  instrumentId: string
  fromDay: number
  toDay: number
  fromMonth: number
  toMonth: number
}

class StockFetcher {
  tinkoffFetchStockData = async (options: tinkoffFetchStockData) => {
    const apiKey: string | undefined = config.get("TINKOFF_API_KEY")

    if (!apiKey) throw new Error("Missing Tinkoff API key")

    const { figi, fromDay, fromMonth, instrumentId, interval, toDay, toMonth } =
      options

    const url = `https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.MarketDataService/GetCandles`

    const from = `2024-${convertToCorrectDay(fromMonth)}-${convertToCorrectDay(
      fromDay
    )}T00:00:00Z`

    const to = `2024-${convertToCorrectDay(toMonth)}-${convertToCorrectDay(
      toDay
    )}T00:00:00Z`

    const body = {
      figi,
      from,
      to,
      interval,
      instrumentId,
    }

    const response: AxiosResponse<ITinkoffResponse> = await axios.post(
      url,
      body,
      {
        headers: {
          Authorization: `Bearer ${apiKey}`,
        },
      }
    )

    const data = transformData(response.data)

    return data
  }
}

const stockFetcher = new StockFetcher()

export default stockFetcher
