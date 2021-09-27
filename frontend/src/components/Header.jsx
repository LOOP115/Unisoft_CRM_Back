import React from "react";


function Header(){
    const headerStyle = {
        textAlign: "center",
      };
    
      return (
        <header style = {headerStyle}><br/ ><h1>Client Relationship Management System</h1> </header>       
      );
}



function firstButton(){
  return (<button className = "btn1">Sign up</button>);
}


function secondtButton(){
  return (<button className = "btn2">Log in</button> );
}

export default Header;
export {firstButton, secondtButton};