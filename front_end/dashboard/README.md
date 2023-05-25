# COMP90024 - ASSIGNMENT 2 / DASHBOARD

## Introduction:
Git repository for group 1 project's frontend. The dashboard was built to provide a nice visualization for the stories discovered through analysis of social media data.

## Technologies:
This project was built using React framework and Typescript. Additionaly the following libraries and tools were used:

+ fortawesome/fontawesome-svg-core": "^6.4.0"
+ fortawesome/free-solid-svg-icons": "^6.4.0"
+ fortawesome/react-fontawesome": "^0.2.0"
+ testing-library/jest-dom": "^5.16.5"
+ testing-library/react": "^13.4.0"
+ testing-library/user-event": "^13.5.0"
+ types/jest": "^27.5.2"
+ types/node": "^16.18.25"
+ types/react": "^18.2.0"
+ types/react-dom": "^18.2.1"
+ "pigeon-maps": "^0.21.3"
+ "react": "^18.2.0"
+ "react-dom": "^18.2.0"
+ "react-scripts": "5.0.1"
+ "styled-components": "^5.3.10"
+ "typescript": "^4.9.5"
+ "web-vitals": "^2.1.4"
+ types/styled-components": "^5.1.26"
+ typescript-eslint/eslint-plugin": "^5.59.2"
+ typescript-eslint/parser": "^5.59.2"
+ eslint": "^8.39.0"
+ eslint-plugin-react": "^7.32.2"
+ react-tooltip": "^5.11.2"
+ recharts": "^2.6.2"

## Working Features:
All the charts that are accessible from the side menu and the filter on the first chart are fully functional.

## Not Working Features:
The search bar, notification bell and the user icon are not part of the scope of this project's phase. They have been added for cosmetic purposes and to provide source of inspirations for future
enhancements.

## Instalation: 
This project was built using macOS Ventura 13.3.1 (M1). To run this program you will need to install:
+ Node.js 19.0.0 and above
+ Run `npm install` from root directory to install the dependencies (make sure that package.json and package-lock.json are in the root directory)
+ Have this project's API backend server (comp90024-a2/flask_api/back_end_exposer.py) running.
    + There might need to update the backend server address on config.ts file for proper connection.
+ Have this project's Mastodon Harvested Client (comp90024-a2/HarvestorAndDBLoader/mastodon_harvester.py) running.
+ Have couchDB running with initialised data located at (comp90024-a2/flask_api/data/twitter/twitter.json)
+  `npm start` to run the application on localhost.

## Docker:
In the root directory there is a Dockerfile used to build docker image for automated deployment.

## Group Members:
+ Mohammed Nasir:1345586
+ Elena Pashkina:1141034
+ Ellen Morwitch: 1257182
+ Felipe Leefu Huang Lin: 1202652
+ Nicholas Barry: 587667