import React from "react";
import Footer from "./Footer";
import Header, {firstButton, secondtButton}  from "./Header";
import Info from "./Information";
import CallHomePage from "./CallHomePage"
import Login from "./Login"
import Signup from "./Signup";
import Success from "./Success";
import { BrowserRouter, Route, Switch } from 'react-router-dom'
import 'bootstrap/dist/css/bootstrap.min.css'
//import AddCard from "./AddCard";


export const EndPointContext = React.createContext()

function App() {

    const URLEnd = "http://localhost:5000"
    return (
        <div className="App">
            <BrowserRouter>
                <EndPointContext.Provider value={URLEnd}>
                    <Switch>

                        <Route exact path="/">
                            <CallHomePage/>
                        </Route>

                        <Route exact path="/signup">
                            <Signup/>
                        </Route>

                        <Route exact path="/login">
                            <Login/>
                        </Route>

                        <Route exact path="/success">
                            <Success/>
                        </Route>

                    </Switch>
                </EndPointContext.Provider>
            </BrowserRouter>
        </div>
  );
}
export default App;
