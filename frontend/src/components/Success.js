import React, {useContext, useState} from "react";
import {Button} from "react-bootstrap";
import { Redirect } from "react-router-dom";
import Cookies from 'js-cookie';
import { EndPointContext } from './App'



function Success(props){

    const URLEndContext = useContext(EndPointContext)
    const logoutURL = URLEndContext + '/logout'

    const [redirect, setRedirect] = useState(false)

    function handleClick(){
        fetch(logoutURL, {method:'GET', credentials:'include', headers: {
                'Content-Type': 'application/json'
            }}).then
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
                {localStorage.getItem("username")}
            </h2>
            <Button onClick={handleClick}>Logout</Button>
        </div>
    )
}

export default Success