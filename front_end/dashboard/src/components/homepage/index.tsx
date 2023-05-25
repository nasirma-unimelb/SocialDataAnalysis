import React from "react";
import styled from "styled-components";
import homeBackground from '../../common/home-background.jpg'

const Background = styled.div`
  align-items: center;
  background-image: ${`url(${homeBackground})`};
  border-radius: 10px;
  background-size: cover;
  display: flex;
  flex-direction: column;
  height: 100%;
  justify-content: center;
  opacity: 0.5;
  width: 80vw;
`

const Greeting = styled.p`
  font-size: 2rem;
  margin-bottom: 0;
  text-align: center;
`

function HomePage() {
    return (
        <Background>
            <Greeting>
              Cloud is about how you do computing, not where you do computing.
              <br></br>
              <i><strong>Paul Maritz</strong></i>
            </Greeting>
            <p style={{ fontSize: '1.2rem' }}>Select an option from the menu to start</p>
        </Background>
    )
}

export default HomePage;