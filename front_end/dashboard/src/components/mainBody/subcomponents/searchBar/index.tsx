import React from "react";
import styled from "styled-components";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBars, faBell, faMagnifyingGlass, faUser } from '@fortawesome/free-solid-svg-icons'
import { Tooltip } from 'react-tooltip';

const Bar = styled.div`
  align-items: center;
  display: flex;
  justify-content: space-between;
  background-color: var(--primary);
  box-shadow: var(--shadow);
  height: 12.90vh;
  width: 100%;
`
 
const LeftBox = styled.div`
  display: flex;
  margin: 0 0 0 40px;
`
const RightBox = styled.div`
  display: flex;
  margin: 0 60px 0 0;
`
const Text = styled.text`
  color: var(--purple);
  margin: 0 0 0 1rem;
  padding-bottom: 10px;
`

const SearchBar = () => {
    return (  
        <Bar>
            <LeftBox>
              <FontAwesomeIcon icon={faBars} style={{ color: 'var(--purple)' }} size="lg"  />
              <FontAwesomeIcon className="search" icon={faMagnifyingGlass} style={{ color: 'var(--purple)', marginLeft: '30px' }} size="lg"  />
              <Text>Search</Text>
              <Tooltip 
                anchorSelect='.search'
                place="right"
                >
                <p style={{ fontWeight:'bold' }}>Stay tuned for next release!</p>
              </Tooltip>
            </LeftBox>
            <RightBox>
              <FontAwesomeIcon icon={faBell} style={{ color: 'var(--purple)', marginRight: '30px' }} size="xl"  /> 
              <FontAwesomeIcon icon={faUser} style={{ color: 'var(--purple)' }} size="lg"  /> 
            </RightBox>
        </Bar>
    );
}
 
export default SearchBar;