import React from 'react';
import GlobalStyle from './GlobalStyle';
import './App.css';
import Dashboard from './pages/dashboard';
import { ErrorProvider } from './hooks/errorProvider'; 
import { FilterProvider } from './hooks/filterProvider';

function App() {
  return (
    <>
      <GlobalStyle />
      <ErrorProvider>
      <FilterProvider>
        <Dashboard/>
      </FilterProvider>
      </ErrorProvider>
    </>
  );
}

export default App;
