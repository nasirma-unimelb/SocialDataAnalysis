import React, { createContext, useState } from "react";

interface MyContextType {
  selection: string;
  setSelection: React.Dispatch<React.SetStateAction<string>>;
}

const FilterContext = createContext<MyContextType>({
  selection: '',
  setSelection: Object
});

function FilterProvider({ children } : { children : JSX.Element }) {
  const [selection, setSelection] = useState('');

  const contextValue: MyContextType = {
    selection,
    setSelection,
  };

  return (
    <FilterContext.Provider value={contextValue}>
      {children}
    </FilterContext.Provider>
  );
}

export { FilterProvider, FilterContext};