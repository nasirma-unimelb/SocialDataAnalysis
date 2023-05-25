import React, { useContext, useEffect, useState } from 'react';
import { BarChart, XAxis, YAxis, CartesianGrid, Bar, Tooltip, Legend } from 'recharts';
import { MastodonChartMastData, MastodonChartTweetData } from '../../../../../types/graphDataTypes';
import { fetchApi } from '../../../../../utils/api';
import { endpoints } from '../../../../../utils/endpoints';
import Spinner from '../../../../spinner';
import { ErrorContext } from "../../../../../hooks/errorProvider";

function MastodonChart()  {
    const [graphData, setGraphData] = useState({} as MastodonChartMastData);
    const [tweetData, setTweetData] = useState({} as MastodonChartTweetData);
    const [isLoading, setIsLoading] = useState(true);
    const { setError } = useContext(ErrorContext);

    useEffect(() => {
        const fetchTweetData = async () => {
          const data : MastodonChartTweetData = await fetchApi(endpoints['mastodonChartT'])
          if (data instanceof Error) {
            return setError(true);
          }

          data.data.sort((a: { bin: string; }, b: { bin: string; }) => {
            const binA = parseFloat(a.bin.split(" / ")[0]);
            const binB = parseFloat(b.bin.split(" / ")[0]);
          
            if (binA < binB) {
              return -1;
            } else if (binA > binB) {
              return 1;
            } else {
              return 0;
            }
          });
  
          setTweetData(data)
        }
        fetchTweetData();

        const fetchData = async () => {
            const data : MastodonChartMastData = await fetchApi(endpoints['mastodonChart'])
            if (data instanceof Error) {
              return setError(true);
            }
    
            data.mastodonSentiments.data.sort((a: { bin: string; }, b: { bin: string; }) => {
                const binA = parseFloat(a.bin.split(" / ")[0]);
                const binB = parseFloat(b.bin.split(" / ")[0]);
              
                if (binA < binB) {
                  return -1;
                } else if (binA > binB) {
                  return 1;
                } else {
                  return 0;
                }
              });
    
            setGraphData(data)
            setIsLoading(false)
          }
          fetchData();
    
          const interval = setInterval(() => {
            fetchData();
          }, 5000);
      
          return () => {
            clearInterval(interval);
          };

      },[])
  
      return (
        isLoading ? <Spinner/> :
        <>
            <BarChart
            width={880} 
            height={290} data={tweetData.data}           
            margin={{
            top: 20,
            right: 20,
            bottom: 20,
            left: 20,
        }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="bin" 
              tick={{ fontSize: 12 }} 
              label={{value:`${tweetData.Label}`, offset:0,  position: "insideBottom"}} 
            />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar 
              dataKey="frequency" 
              fill="#82ca9d" 
              barSize={100} 
            />
        </BarChart>  
        <BarChart
            width={880} 
            height={300} data={graphData.mastodonSentiments.data}           
            margin={{
            top: 20,
            right: 20,
            bottom: 20,
            left: 20,
        }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="bin" 
              tick={{ fontSize: 12 }} 
              label={{value:`${graphData.mastodonSentiments.Label}`, offset:0,  position: "insideBottom"}} 
            />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="frequency" fill="#8884d8" barSize={100} />
        </BarChart> 
    </>
      );
  }

export default MastodonChart;