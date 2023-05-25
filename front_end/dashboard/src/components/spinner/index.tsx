import React from 'react';
import spinner from '../../common/spinner.gif'

function Spinner() {
  return (
    <div style={{ display: 'flex', flexDirection:'column', justifyContent: 'center',  height: '100%', width: '100%'}}>
      <img
        src={spinner}
        style={{ width: '100', margin: 'auto', display: 'block', height: '100px' }}
      />
    </div>
  );
} 

export default Spinner;

