import React from "react";

function Footer(){
    const currentYear = new Date().getFullYear();

    const footerStyle ={
        backgroundColor : "#4A403A",
        color : "lightGray",
        textAlign : "center",
        height: "50px",
        margin: "0px 0px 0px 0px",
    };

    return (
        <p style = {footerStyle}><p><br />Copyright © {currentYear} by: Team Unisoft</p></p>
    );       
}

export default Footer;