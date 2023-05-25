import React, { useContext, useState} from 'react';
import styled from 'styled-components';
import { FilterContext } from '../../hooks/filterProvider';

const FilterBox: React.FC = () => {
const { setSelection } = useContext(FilterContext);
  const [selectedSentiment, setSelectedOption] = useState<string>('');
  const handleRadioChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedOption(event.target.value);
    setSelection(event.target.value);
  };
  const sentimentTypes = ['negative', 'neutral', 'positive']

  const Container = styled.div`
    margin: 10px 40px 20px 40px;
  `

  return (
    <>
        <h3 style={{margin: '20px 40px 5px 45px', color: 'var(--purple)' }}>Filter by Sentiment</h3>
        <Container>
            <label key="all" style={{ color: 'var(--purple)' }}>
                <input
                type="radio"
                name="sentiment"
                value="all"
                checked={selectedSentiment == "all"}
                onChange={handleRadioChange}
                key="all"
                />
            all
            </label>
        {sentimentTypes.map((sentimentType) => (
                <label key={sentimentType} style={{ color: 'var(--purple)' }}>
                    <input
                    type="radio"
                    name="sentiment"
                    value={sentimentType}
                    checked={selectedSentiment == `${sentimentType}`}
                    onChange={handleRadioChange}
                    key={sentimentType}
                    />
                {sentimentType}
                </label>
        ))}
        </Container>
    </>
  );
};

export default FilterBox;
