import React from "react";
import Footer from "./Footer";
import Header, {firstButton, secondtButton}  from "./Header";
import Info from "./Information";

import AddCard from "./AddCard";




function App() {
    const headerStyle = {
        margin: "auto",
        width : "auto",
        backgroundColor: "#F7F6F2",
        height: "300px",
        bottom : "0px",    
        textAlign: "center", 
    };
    

    const wholeColor = {
        backgroundColor:"#F7F6F2",
    }
    return (
    <div style = {wholeColor}>
        <div style = {headerStyle}>
        <Header />
        < br/>
        {firstButton()}
        {"- or -"}
        {secondtButton() }
        </div>
        <Info />
        <AddCard />
        <Footer />
    </div>
  );
}
export default App;
