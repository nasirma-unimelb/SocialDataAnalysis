import React, { useEffect, useState, useContext } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { BarData } from '../../../../../types/graphDataTypes';
import { fetchApi, filterApi } from '../../../../../utils/api';
import { endpoints } from '../../../../../utils/endpoints';
import Spinner from '../../../../spinner';
import { ErrorContext } from "../../../../../hooks/errorProvider";
import { FilterContext } from '../../../../../hooks/filterProvider';
import FilterBox from '../../../../filterBox';

export default function BarChartTopics()  {
  const [graphData, setGraphData] = useState({} as BarData);
  const [isLoading, setIsLoading] = useState(true);
  const barColor = ["#d16f69", "#767878", "#8884d8", "#82ca9d", "#FCD12A"]
  const { setError } = useContext(ErrorContext);
  const { selection } = useContext(FilterContext);

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchApi(endpoints['barChartTopics'])
      if (data instanceof Error) {
        return setError(true);
      }
      setGraphData(data)
      setIsLoading(false)
    }
    fetchData();
  },[])

  useEffect(() => {
    if (selection == '') return

    if (selection == 'all') {
      const fetchData = async () => {
        const data = await fetchApi(endpoints['barChartTopics'])
        if (data instanceof Error) {
          return setError(true);
        }
        setGraphData(data)
        setIsLoading(false)
      }
      fetchData();
    } else {
      const fetchData = async () => {
        const data = await filterApi(endpoints['barChartTopicsFilter'], selection)
        if (data instanceof Error) {
          return setError(true);
        }
        setGraphData(data)
        setIsLoading(false)
      }
      fetchData();
    }
  },[selection])

    return (
      <>
        {isLoading ? <Spinner/> :
        <>
          <FilterBox />
          <ResponsiveContainer width="100%" height="80%">
          <BarChart
            width={500}
            height={300}
            data={graphData.data}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={`${graphData.meta.xLabel}`}  label={{ value: graphData.meta.xLabel, offset:0,  position: "insideBottom" }}/>
            <XAxis
              dataKey="date"
              axisLine={false}
              tickLine={false}
              interval={0}
              height={1}
              scale="band"
              xAxisId="quarter"
            />
            <YAxis label={{ angle:-90, value: graphData.meta.yLabel, offset:0,  position: "left" }} />
            <Tooltip />
            <Legend />
            {graphData.meta.barLabels.map((label, index) => (
              <Bar dataKey={label} fill={barColor[index]} key={label} />
            ))}
          </BarChart>
        </ResponsiveContainer>
        </>
        }
      </>
    );
}