export interface ICandleResponse {
  open: { units: string; nano: number }
  high: { units: string; nano: number }
  low: { units: string; nano: number }
  close: { units: string; nano: number }
  volume: string
  time: string
  isComplete: boolean
  candleSource: string
}
export interface ITinkoffResponse {
  candles: ICandleResponse[]
}
