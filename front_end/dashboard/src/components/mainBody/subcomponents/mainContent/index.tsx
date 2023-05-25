import React from "react";
import BarChartTopics from "./subcomponents/barChartTopics";
import LinearBarChartIrate from "./subcomponents/linearBarChartIRate";
import LinearBarChartHouse from "./subcomponents/linearBarChartHouse";
import MapView from "./subcomponents/mapView";
import ScatterPlotMortgate from "./subcomponents/scatterPlotMortgage";
import ScatterPlotOwnership from "./subcomponents/scatterPlotOwnership";
import MastodonChart from "./subcomponents/mastodonChart";
import LinearBarChartInflation from "./subcomponents/linearBarChartInflation";
import HomePage from "../../../homepage";

const MainContent = ({ selection }: { selection : string } ) => {
    if (selection == "barChartTopics") return <BarChartTopics/>
    if (selection == "linearBarChartIrate") return <LinearBarChartIrate/>
    if (selection == "linearBarChartHouse") return <LinearBarChartHouse /> 
    if (selection == "linearBarChartInflation") return <LinearBarChartInflation/>
    if (selection == "scatterPlotMortgage") return <ScatterPlotMortgate />
    if (selection == "scatterPlotOwnership") return <ScatterPlotOwnership />
    if (selection == "map") return <MapView />
    if (selection == "mastodonChart") return <MastodonChart />

    return <HomePage/>
}
 
export default MainContent;