import React from "react";
import Footer from "./Footer";
import Header, {firstButton, secondtButton}  from "./Header";
import Info from "./Information";
import CallHomePage from "./CallHomePage"
import Login from "./Login"
import Signup from "./Signup";
import { BrowserRouter, Route, Switch } from 'react-router-dom'
//import AddCard from "./AddCard";


export const EndPointContext = React.createContext()

function App() {

    const URLEnd = "unisoft-app.herokuapp.com"
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

                    </Switch>
                </EndPointContext.Provider>
            </BrowserRouter>
        </div>
  );
}
export default App;
