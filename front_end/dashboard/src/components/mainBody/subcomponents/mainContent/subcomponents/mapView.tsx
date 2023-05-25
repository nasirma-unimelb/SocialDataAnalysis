import React, {useContext, useEffect, useState} from "react"
import { Map, Marker } from "pigeon-maps"
import { Tooltip } from 'react-tooltip';
import 'react-tooltip/dist/react-tooltip.css';
import { GCCMAP } from "../../../../../utils/gccMap";
import { MapPoints } from "../../../../../types/graphDataTypes";
import { fetchApi } from '../../../../../utils/api';
import { endpoints } from '../../../../../utils/endpoints';
import Spinner from '../../../../spinner';
import { ErrorContext } from "../../../../../hooks/errorProvider";

export function MapView() {
  const color = '#c79796'
  const[mapData, setMapData] = useState({} as MapPoints[]);
  const [isLoading, setIsLoading] = useState(true);
  const { setError } = useContext(ErrorContext);

  useEffect(() => {
    const fetchData = async () => {
      const data : MapPoints[] = await fetchApi(endpoints['mapView'])
      if (data instanceof Error) {
        return setError(true);
      }  
      setMapData(data)
      setIsLoading(false)
    }
    fetchData();
  },[])

  return (
    isLoading ? <Spinner/> :
    <Map height={550} defaultCenter={[-28.96, 132.83]} defaultZoom={4.4}>
        {  mapData.map((datapoint, index) => (
            <Marker 
              // width={50}
              width={datapoint.tweets < 100 ? 20 : datapoint.tweets  < 1000 ? 50 : 80 }
              anchor={GCCMAP[datapoint.gcc].coordinates} 
              color={color} 
              className={`gcc-${datapoint.gcc}`}
              key={index}
            />
        ))}
        {mapData.map((datapoint, index) => (
            <Tooltip 
              anchorSelect={`.gcc-${datapoint.gcc}`}
              place="right"
              style={{ backgroundColor:"var(--iceBlue)", color: "#222" }}
              key={index}
              >
              <p style={{ fontWeight:'bold' }}>{`Region: ${GCCMAP[datapoint.gcc].denomination}`}</p>
              <p>{`Number of Tweets: ${datapoint.tweets}`}</p>
            </Tooltip>
        ))}
    </Map>
  )
}

export default MapView;