import styled from "styled-components";

export const OuterContainer = styled.body`
  display: flex;
  flex-direction: column;
  width: 100%;
`

export const MainContentContainer = styled.div`
  display: flex;
  height: 100%;
  gap: 20px;
  margin: 30px 30px 10px 30px;
  width: 100%;
`

export const VisualContainer = styled.div`
  background: var(--primary); 
  border-radius: 10px;
  width: 70%;
  padding: 20px;
`

export const DetailViewContainer = styled.div`
  background: var(--iceBlue);
  border-radius: 10px;
  font-size: 1.2rem;
  font-family: monospace;
  font-weight: 600;
  height: 100%;
  line-height: 2.6rem;
  margin-left: 30px;
  padding: 2rem;
  width: 20%;
`