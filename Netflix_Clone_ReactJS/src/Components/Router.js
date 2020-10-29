import React from "react";
import {BrowserRouter as Router, Route, Redirect, Switch} from "react-router-dom";
import Home from "../Routers/Home";
import TV from "../Routers/TV";
import Search from "../Routers/Search";



export default () => (
    <Router>
        <Switch>
            <Route path="/" exact component={Home}/>
            <Route path="/TV" exact component={TV}/>
            <Route path="/TV/popular" render ={() => <h1>Popular</h1>} />
            <Route path="/Search" component={Search}/>
            
            <Redirect from="*" to="/" />
        </Switch>
    </Router>

)