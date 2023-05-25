import React, { useState } from 'react';
import styled from 'styled-components';
import MainBody from '../mainBody';
import Menu from '../menu';

const Container = styled.div`
    background: var(--background);
    display: flex;
    height: 100vh;
`

function Main() {
    const [selection, setSelection] = useState('');

    const updateSelection = (selection : string) => {
        setSelection(selection);
    };

    return(
        <Container>
            <Menu onClick={(selection : string) => updateSelection(selection) }/>
            <MainBody selection={selection} />
        </Container>    
    )
}

export default Main;