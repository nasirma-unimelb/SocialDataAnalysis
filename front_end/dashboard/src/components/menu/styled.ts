import styled from "styled-components";

export const Container = styled.div`
  background-color: var(--accent);
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 18vw;
`
export const Logo = styled.div`
  align-items: center;
  display: flex;
  justify-content: center;
  background-color: var(--accent);
  height: 10vh;
  box-shadow: var(--shadow);
  width: 100%;
`

export const ItemContainer = styled.div`
  display: flex;
  flex-direction: row;
  margin-bottom: 1rem;
  margin-left: 1rem;
`

export const MenuSelection = styled.div`
  padding: 1rem;
`

export const Title = styled.h3`
  color: var(--text-secondary);
`