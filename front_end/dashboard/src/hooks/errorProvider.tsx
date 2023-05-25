import React, { createContext, useState } from "react";

interface MyContextType {
  hasError: boolean;
  setError: React.Dispatch<React.SetStateAction<boolean>>;
}

const ErrorContext = createContext<MyContextType>({
  hasError: false,
  setError: Object
});

function ErrorProvider({ children } : { children : JSX.Element }) {
  const [hasError, setError] = useState(false);

  const contextValue: MyContextType = {
    hasError,
    setError,
  };

  return (
    <ErrorContext.Provider value={contextValue}>
      {children}
    </ErrorContext.Provider>
  );
}

export { ErrorProvider, ErrorContext};