import React from "react";
import styled from "styled-components";

const FooterContent = styled.footer`
    background-color: transparent;
    color: var(--text-primary);
    padding: 10px;
    width: 100%;
`

const Footer = () => {
    return (  
        <FooterContent>
            <p style={{textAlign:"center"}}>
              &copy;Comp90024-Group1-2023S1
            </p>
        </FooterContent>
    );
}
 
export default Footer;