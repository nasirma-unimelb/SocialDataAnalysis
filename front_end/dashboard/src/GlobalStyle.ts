import { createGlobalStyle } from 'styled-components';

const GlobalStyle = createGlobalStyle`
  body * {
    box-sizing: border-box;
    text-align: left;
  }
  body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
      'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
      sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: var(--text-primary);
  }
    
  :root {
    --background: #F2F3F8;
    --text-primary: #000;
    --text-secondary: #dcdcdc;
    
    --primary: white;
    --accent: #2D324B;
    --purple: #592693;
    --iceBlue: #E7EDF7;

    --shadow: rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px;

  }
`;

export default GlobalStyle;