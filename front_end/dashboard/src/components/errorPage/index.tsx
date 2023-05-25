import React from "react";
import styled from "styled-components";
import homeBackground from '../../common/error_page.jpg'

const Background = styled.div`
  align-items: center;
  background-image: ${`url(${homeBackground})`};
  border-radius: 10px;
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
  display: flex;
  flex-direction: column;
  height: 100%;
  justify-content: center;
  opacity: 0.5;
  width: 100%;
`

function ErrorPage() {
    return (
        <Background/>
    )
}

export default ErrorPage;