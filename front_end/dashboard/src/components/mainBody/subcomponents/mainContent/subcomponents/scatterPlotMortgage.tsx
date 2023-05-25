import React, { useContext, useEffect, useState } from 'react';
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  ZAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,

} from 'recharts';
import { ScatterPlotData } from '../../../../../types/graphDataTypes';
import { fetchApi } from '../../../../../utils/api';
import { endpoints } from '../../../../../utils/endpoints';
import Spinner from '../../../../spinner';
import { ErrorContext } from "../../../../../hooks/errorProvider";

export default function ScatterPlotMortgate()  {
  const [graphData, setGraphData] = useState({} as ScatterPlotData);
  const [isLoading, setIsLoading] = useState(true);
  const { setError } = useContext(ErrorContext);

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchApi(endpoints['scatterPlotMortgage'])
      if (data instanceof Error) {
        return setError(true);
      }
      setGraphData(data)
      setIsLoading(false)
    }
    fetchData();
  },[])

    return (
      <>
        {isLoading ? <Spinner/> :
        <>
          <ResponsiveContainer width="100%" height={560}>
            <ScatterChart
              margin={{
                top: 20,
                right: 20,
                bottom: 20,
                left: 20,
              }}
            >
              <CartesianGrid />
              <XAxis 
                type="number" 
                dataKey={`${graphData.meta.xLabel}`} 
                name={`${graphData.meta.xLabel}`} 
                domain={[1100, 2200]} 
                label={{ value: graphData.meta.xLabel, offset:5, position: "insideBottom" }}
              />
              <YAxis 
                type="number" 
                dataKey={`${graphData.meta.yLabel}`} 
                name={`${graphData.meta.yLabel}`} 
                domain={[0, 2]}
                label={{ angle:-90, value: graphData.meta.yLabel, offset:0,  position: "left" }}   
              />
              <ZAxis type="category" dataKey={`${graphData.meta.zLabel}`} name={`${graphData.meta.zLabel}`} />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} />
              <Legend />
              <Scatter 
                name={graphData.meta.categories[0]} 
                data={graphData.metropolitan} 
                fill="#8884d8" 
                shape="star"
              >
                {/* <LabelList dataKey={`${graphData.meta.zLabel}`}/> */}
              </Scatter>  
              <Scatter 
                name={graphData.meta.categories[1]} 
                data={graphData.rural} 
                fill="#82ca9d" 
                shape="triangle"
              >
                {/* <LabelList dataKey={`${graphData.meta.zLabel}`}/> */}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>  
        </>
        }
      </>
    );
}