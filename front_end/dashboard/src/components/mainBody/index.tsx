import React, {useContext} from "react";
import { DetailViewContainer, VisualContainer, MainContentContainer, OuterContainer } from "./styled";
import SearchBar from "./subcomponents/searchBar";
import Footer from "../footer";
import MainContent from "./subcomponents/mainContent";
import HomePage from "../homepage";
import { ErrorContext } from "../../hooks/errorProvider";
import ErrorPage from "../errorPage";
import { TitleMap } from "../../utils/constants";
import FilterBox from "../filterBox";

const MainBody  = ({ selection }: { selection : string }) => {
  const { hasError } = useContext(ErrorContext);

  const menuOptions = ['barChartTopics', 'linearBarChartIrate', 
  'linearBarChartHouse', 'linearBarChartInflation', 'scatterPlotMortgage', 'scatterPlotOwnership', 'map', 'mastodonChart']

    return (  
        <OuterContainer>
            <SearchBar/>
            <MainContentContainer>
              {
                hasError ? <ErrorPage /> :
                !menuOptions.includes(selection) ? 
                <HomePage /> :
                <>                
                  <VisualContainer>
                    <h3 style={{margin: 0, textAlign: 'center'}} >{ TitleMap[ selection as keyof typeof TitleMap ] }</h3>
                    <MainContent selection={selection} />
                  </VisualContainer>
                  {selection == 'barChartTopics' ?
                  <DetailViewContainer>
                    The volume of tweets overall had spiked between weeks 16 and 20, especially for “interest rates”, “inflation” and “housing” topics. 
                    What happened?
                  </DetailViewContainer> 
                  : selection == 'linearBarChartIrate' ?
                  <DetailViewContainer>
                    Big boost in volume of tweets in weeks 18 & 23 when the first few interest hikes were announced. 
                    Also a spike in week 15 - probably in anticipation of the interest hike announcement.
                  </DetailViewContainer> 
                  : selection == 'linearBarChartInflation' ?
                  <DetailViewContainer>
                    The volume of tweets have spiked after the official inflation figures reversed a temporary drop in week 18.
                  </DetailViewContainer> 
                  : selection == 'linearBarChartHouse' ?
                  <DetailViewContainer>
                    Big boost in volume of tweets two weeks leading up to and two weeks post the first rate hike announcement.
                  </DetailViewContainer> 
                  : selection == 'scatterPlotMortgage' ?
                  <DetailViewContainer>
                    A larger mortgage correlates with a higher proportion of the population tweeting about interest rates.
                  </DetailViewContainer> 
                  : selection == 'scatterPlotOwnership' ?
                  <DetailViewContainer>
                    When people own their home outright (i.e. no mortgage) they are less likely to tweet about interest rates.
                  </DetailViewContainer> 
                  : selection == 'map' ?
                  <DetailViewContainer>
                    Mouse over a Greater Capital City Statistical Area to see tweet volume in that area.
                  </DetailViewContainer> 
                  : selection == 'mastodonChart' ?
                  <DetailViewContainer>
                    Comparing tweet/toot sentiment between Twitter (Feb-Aug 2022) and Mastodon (real time).
                    Sentiment ranges between -1 (negative) and 1 (positive); 0 is neutral.
                  </DetailViewContainer> :
                  <DetailViewContainer>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatibus laudantium 
                    sed dignissimos totam provident expedita veniam itaque mollitia nemo aliquid! In ducimus 
                    recusandae facere qui consequuntur deleniti officiis, consectetur voluptates.
                  </DetailViewContainer> }
                </>
              }
            </MainContentContainer>
            <Footer/>
        </OuterContainer>
    );
}
 
export default MainBody;
