import React from "react";
import styled from "styled-components";

const Button = styled.button<{$margin?: string}>`
    background-color: transparent;
    border: 0;
    color: var(--text-secondary);
    &:hover {
        color: #f8f8ff;
        cursor: pointer;
    };
    margin: ${ props => props.$margin ? props.$margin : 0 };
`

function LinkButton({label, margin, onClick} : { label: string; margin?:string; onClick: React.MouseEventHandler<HTMLButtonElement> }) {
        return (  
            <Button $margin={margin} onClick={onClick}>
                {label}
            </Button>
        );
    }
export default LinkButton;