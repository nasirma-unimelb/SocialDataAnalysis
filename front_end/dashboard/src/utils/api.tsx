import { DEV_API_PREFIX, DEMO_API_PREFIX} from "../config";

export async function fetchApi (endpoint : string) {

    try {
        const response = await fetch(`${DEV_API_PREFIX}/${endpoint}`)
        if (!response.ok) {
          throw new Error('Request failed with status ' + response.status);
        }
        return response.json();
      } catch (error) {
        console.log('Error fetching data:', error);
        return error;
    }
}

export async function filterApi (endpoint : string, selection : string ) {
    const data = {
      "sentiment" : selection
    }

    const body = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    }

    try {
      const response = await fetch(`${DEV_API_PREFIX}/${endpoint}`, body)
      if (!response.ok) {
        throw new Error('Request failed with status ' + response.status);
      }
      return response.json();
    } catch (error) {
      console.log('Error fetching data:', error);
      return error;
  }
}
