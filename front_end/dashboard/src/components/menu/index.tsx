import React, { useContext } from 'react';
import { Container, Logo, MenuSelection, Title, ItemContainer } from "./styled";
import LinkButton from "../linkButton";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faChartLine, faChartBar, faCompass, faMapLocationDot, faCommentDollar, faHouse, faM } from '@fortawesome/free-solid-svg-icons'
import { ErrorContext } from "../../hooks/errorProvider";

const Menu = ({ onClick }: { onClick: ( selection : string ) => void } ) => {
    const { setError } = useContext(ErrorContext);
    const handleClick = (selection: string) => {
      onClick(selection);
      setError(false)
    };

    return (  
        <>
          <Container>
            <Logo>
              <FontAwesomeIcon icon={faCompass} style={{ color: 'var(--text-secondary)'}} size="3x" />
            </Logo>
            <br></br>
            <MenuSelection>
              <Title>CHARTS</Title>
              <ItemContainer>
                <FontAwesomeIcon icon={faChartBar} style={{ color: 'var(--text-secondary)' }} />
                <LinkButton label="Tweets by Topics" margin={ '0 0 0 0.4rem'} onClick={() => handleClick('barChartTopics')} />
              </ItemContainer>
              <ItemContainer>
                <FontAwesomeIcon icon={faChartLine} style={{ color: 'var(--text-secondary)' }} />
                <LinkButton label='Interest Rate vs RBA Rate Tweets' margin={ '0 0 0 0.4rem'} onClick={() => handleClick('linearBarChartIrate')} />
              </ItemContainer>
              <ItemContainer>
                <FontAwesomeIcon icon={faChartLine} style={{ color: 'var(--text-secondary)' }} />
                <LinkButton label='Interest Rate vs Housing Tweets' margin={ '0 0 0 0.4rem'} onClick={() => handleClick('linearBarChartHouse')} />
              </ItemContainer>
              <ItemContainer>
                <FontAwesomeIcon icon={faChartLine} style={{ color: 'var(--text-secondary)' }} />
                <LinkButton label='Inflation Rate vs Inflation Tweets' margin={ '0 0 0 0.4rem'} onClick={() => handleClick('linearBarChartInflation')} />
              </ItemContainer>
              <ItemContainer>
                <FontAwesomeIcon icon={faCommentDollar} style={{ color: 'var(--text-secondary)' }} />
                <LinkButton label="Mortgage vs RBA Rate Tweets" margin={ '0 0 0 0.4rem'} onClick={() => handleClick('scatterPlotMortgage')} />
              </ItemContainer>
              <ItemContainer>
                <FontAwesomeIcon icon={faHouse} style={{ color: 'var(--text-secondary)' }} />
                <LinkButton label="Ownership vs RBA Rate Tweets" margin={ '0 0 0 0.4rem'} onClick={() => handleClick('scatterPlotOwnership')} />
              </ItemContainer>
              <Title>MAPS</Title>
              <ItemContainer>
                <FontAwesomeIcon icon={faMapLocationDot} style={{ color: 'var(--text-secondary)' }} />
                <LinkButton label="Map View" margin={ '0 0 0 0.4rem'} onClick={() => handleClick('map')} />
              </ItemContainer>
              <Title>MASTODON</Title>
              <ItemContainer>
                <FontAwesomeIcon icon={faM} style={{ color: 'var(--text-secondary)' }} />
                <LinkButton label="Mastodon Analysis" margin={ '0 0 0 0.4rem'} onClick={() => handleClick('mastodonChart')} />
              </ItemContainer>
            </MenuSelection>
          </Container>
        </>
    );
}
 
export default Menu;