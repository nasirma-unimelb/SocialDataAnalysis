// Linear Bar Chart
type LinearBarMeta = {
  xLabel: string,
  leftYLabel: string,
  rightYLabel: string
}

type LinearBarFeatures = {
  xAxis: number,
  leftYAxis: number,
  rightYAxis: number,
}

export interface LinearBarData {
  meta: LinearBarMeta,
  data: LinearBarFeatures[]
}

// Bar Chart
type BarMeta = {
  xLabel: string,
  yLabel: string,
  barLabels: string[]
}

type BarFeatures = {
  feature1: number,
  feature2: number,
  feature3: number,
  feature4: number,
  feature5: number,
}

export interface BarData {
  meta: BarMeta,
  data: BarFeatures[]
}

// Scatter Plot
type ScatterPlotMeta = {
  xLabel: string,
  yLabel: string,
  zLabel: string,
  categories: [string, string]
} 

type ScatterPlotDataPoint = {
  label: string,
  xAxis: number,
  yAxis: number
}

type ScatterPlotFeature = ScatterPlotDataPoint[]

export interface ScatterPlotData {
  meta: ScatterPlotMeta,
  metropolitan: ScatterPlotFeature,
  rural: ScatterPlotFeature
}

// Map View
export type MapPoints = {
  gcc: string,
  tweets: number
}

// Mastodon Chart
type SentimentData = {
  bin: string, frequency: number
}

type SentimentObject = {
  Label: string, data: SentimentData[]
}

export interface MastodonChartMastData {
  mastodonSentiments: SentimentObject,
}

export type MastodonChartTweetData = {
  Label: string, data: SentimentData[]
}