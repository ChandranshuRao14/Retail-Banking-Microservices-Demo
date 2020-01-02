import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

/* Import Views for Retail Banking App */
import Home from "./views/home";
import Transfer from "./views/transfer";
import Transactions from "./views/transactions";
import { slide as Menu } from 'react-burger-menu';
import menuStyles from "./components/Menu"
import profileStyles from "./components/Profile"
import Header from "./components/layout/Header"
import Avatar from '@material-ui/core/Avatar'
import { makeStyles } from '@material-ui/core/styles';
/* Style Sheet */
import "./styles/app.css";

const useStyles = makeStyles(theme => ({
  yellow: {
    color: '#4285F4',
    backgroundColor: '#fff',
  },
}));

const App: React.FC = () => {
  const classes = useStyles();
  return (
    <Router>
      <div className="App">

        <Menu disableAutoFocus styles={ menuStyles }>
          <a id="Transfer History" className="menu-item" href="/">Home</a>
          <a id="Transfer History" className="menu-item" href="/transfer">Transfer</a>
          <a id="Transaction History" className="menu-item" href="/transactions">Transactions</a>
        </Menu>  

        <Menu right customBurgerIcon={ <Avatar className={classes.yellow}>H</Avatar> } styles={ profileStyles }>
          <a id="Transfer History" className="menu-item" href="/">Username</a>
          <a id="Transaction History" className="menu-item" href="/about">Email</a>
          <a id="Transaction History" className="menu-item" href="/about">Account balance</a>
          <a id="Transaction History" className="menu-item" href="/about">Address</a>
        </Menu>

        <Header></Header>

        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
          <Route path="/transfer">
            <Transfer />
          </Route>
          <Route path="/transactions">
            <Transactions />
          </Route>
        </Switch>
      </div>
    </Router>
  );
};

export default App;
