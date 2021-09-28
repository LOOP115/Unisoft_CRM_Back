import React, {useState} from "react";
import {Button} from "react-bootstrap";
import { Redirect } from "react-router-dom";


function Success(){
    const [redirect, setRedirect] = useState(false)

    function handleClick(){
        fetch("http://127.0.0.1:5000/logout", {method:"GET", credentials:"include"}).then
        (res=>{
                localStorage.clear()
                setRedirect(true)
            }

        )
    }


    if (redirect) return (<Redirect to={"/"}/>)

    return(
        <div>
            <h2>
                {localStorage.getItem("stuff")}
            </h2>
            <Button onClick={handleClick}>Logout</Button>
        </div>
    )
}

export default Success