import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

/* Import Views for Retail Banking App */
import Home from "./views/home";
import Profile from "./views/profile";
import Transfer from "./views/transfer";

/* Style Sheet */
import "./styles/app.css";

/* Components for App */
import Navbar from "./components/navbar";

const App: React.FC = () => {
  return (
    <Router>
      <div className="App">
        <Navbar></Navbar>

        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
          <Route path="/profile">
            <Profile />
          </Route>
          <Route path="/transfer">
            <Transfer />
          </Route>
        </Switch>
      </div>
    </Router>
  );
};

export default App;
