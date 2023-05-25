export interface GCCObject {
    gcc: string;
    coordinates: [number, number];
    denomination: string;
}

export interface GCCMap {
    [key: string]: GCCObject;
  }

export const GCCMAP: GCCMap= {
    '1gsyd': {
        gcc: '1gsyd',
        coordinates: [-33.86, 151.20],
        denomination: 'Greater Sydney' 
    },
    '1rnsw': {
        gcc: '1rnsw',
        coordinates: [-31.50, 146.43],
        denomination: 'Rest of NSW' 
    },
    '2gmel': {
        gcc: '2gmel',
        coordinates: [-37.81, 144.96],
        denomination: 'Greater Melbourne' 
    },
    '2rvic': {
        gcc: '2rvic',
        coordinates: [-36.70, 143.51],
        denomination: 'Rest of Victoria' 
    },
    '3gbri': {
        gcc: '3gbri',
        coordinates: [-27.47, 153.02],
        denomination: 'Greater Brisbane' 
    },
    '3rqld': {
        gcc: '3rqld',
        coordinates: [-24.00, 144.83],
        denomination: 'Rest of Queensland' 
    },
    '4gade': {
        gcc: '4gade',
        coordinates: [-34.92, 138.60],
        denomination: 'Greater Adelaide' 
    },
    '4rsau': {
        gcc: '4rsau',
        coordinates: [-28.96, 134.83],
        denomination: 'Rest of South Australia' 
    },
    '5gper': {
        gcc: '5gper',
        coordinates: [-31.95, 115.86],
        denomination: 'Greater Perth' 
    },
    '5rwau': {
        gcc: '5rwau',
        coordinates: [-26.47, 122.43],
        denomination: 'Rest of Western Australia' 
    },
    '6ghob': {
        gcc: '6ghob',
        coordinates: [-42.88, 147.32],
        denomination: 'Greater Hobart' 
    },
    '6rtas': {
        gcc: '6rtas',
        coordinates: [-42.16, 146.65],
        denomination: 'Rest of Tasmania' 
    },
    '7gdar': {
        gcc: '7gdar',
        coordinates: [-12.46, 130.84],
        denomination: 'Greater Darwin' 
    },
    '7rnte': {
        gcc: '7rnte',
        coordinates: [-20.12, 133.63],
        denomination: 'Rest of Northern Territory' 
    },
    '8acte': {
        gcc: '8acte',
        coordinates: [-35.28, 149.13],
        denomination: 'Australian Capital Territoy' 
    },
}