import { kmeans } from "ml-kmeans"

class SupportResistanceFinder {
  findSupportResistanceLevels = (prices: number[], numClusters: number) => {
    const data = prices.map((price) => [price])

    const result = kmeans(data, numClusters, {})
    const centroids = result.centroids.map((c) => c[0])

    return centroids
  }
}

const supportResistanceFinder = new SupportResistanceFinder()

export default supportResistanceFinder
