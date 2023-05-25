import React, { useContext, useEffect, useState } from 'react';
import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { LinearBarData } from '../../../../../types/graphDataTypes';
import { fetchApi } from '../../../../../utils/api';
import { endpoints } from '../../../../../utils/endpoints';
import Spinner from '../../../../spinner';
import { ErrorContext } from "../../../../../hooks/errorProvider";


export default function LinearBarChartHouse()  {
  const [graphData, setGraphData] = useState({} as LinearBarData);
  const [isLoading, setIsLoading] = useState(true);
  const { setError } = useContext(ErrorContext);

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchApi(endpoints['linearBarChartHouse'])
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
          <ResponsiveContainer width="100%" height="95%">
            <ComposedChart
              width={500}
              height={400}
              data={graphData.data}
              margin={{
                top: 20,
                right: 20,
                bottom: 20,
                left: 20,
              }}
            >
              <CartesianGrid stroke="#f5f5f5" />
              <XAxis 
                dataKey={`${graphData.meta.xLabel}`} 
                label={{ value: graphData.meta.xLabel, 
                offset:0,  
                position: "insideBottom" }} />
              <YAxis 
                dataKey={`${graphData.meta.leftYLabel}`} 
                label={{ angle:-90, value: graphData.meta.leftYLabel, offset:0,  position: "left" }}  
                tickFormatter={(value) => `${value}%`} />
              <YAxis 
                yAxisId='right' 
                dataKey={`${graphData.meta.rightYLabel}`} 
                orientation='right' 
                label={{ angle:90, value: graphData.meta.rightYLabel, offset:0,  position: "right" }} />
              <Tooltip />
              <Legend />
              <Line 
                type='monotone' 
                dataKey={`${graphData.meta.leftYLabel}`} 
                stroke="black" />
              <Bar 
                yAxisId="right" 
                dataKey={`${graphData.meta.rightYLabel}`} 
                barSize={20} 
                fill="#d16f69" />
            </ComposedChart>
          </ResponsiveContainer>
        }
      </>
    );
}
