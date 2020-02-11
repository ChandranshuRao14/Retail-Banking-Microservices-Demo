import React from "react";
import Avatar from '@material-ui/core/Avatar';
import profileStyles from "../styles/ProfileStyle";
import { slide as Menu } from 'react-burger-menu';
import menuStyles from "../styles/MenuStyle";
import {RouteComponentProps} from "react-router";

// Type whatever you expect in 'this.props.match.params.*'
type PathParamsType = {
  userId: string,
}

// Your component own properties
type PropsType = RouteComponentProps<PathParamsType> & {
  someString?: string,
}

const styles = theme => ({
  yellow: {
    color: '#4285F4',
    backgroundColor: '#fff',
  },
});

interface Props {
  classes: any;
}

class Menus extends React.Component<PropsType> {
  state = {
    name: "",
    email: "",
    currentBalance: 0,
    address: "",
  }

  componentDidMount() {
    fetch("http://localhost/user/" + this.props.match.params.userId)
      .then(response => response.json())
      .then(response => this.setState({
        name: response['Username'],
        email: response['Email'],
        currentBalance: response['AccountBalance'],
        address: response['Address']
      }))
      .catch(error => console.log(error));
  }

  render() {
    const { name, currentBalance, email, address } = this.state;
    // const { classes } = this.props;
    return (
      <div>
        <Menu disableAutoFocus styles={menuStyles}>
          <a id="Transfer History" className="menu-item" href="/">Home</a>
          <a id="Transfer History" className="menu-item" href="/transfer">Transfer</a>
          <a id="Transaction History" className="menu-item" href="/transactions">Transactions</a>
        </Menu>        
        {/* <Menu right customBurgerIcon={<Avatar className={classes.yellow}>H</Avatar>} styles={profileStyles}> */}
        <Menu right customBurgerIcon={<Avatar>H</Avatar>} styles={profileStyles}>
          <a id="Transfer History" className="menu-item" href="/"> {name} </a><br/>
          <a id="Transaction History" className="menu-item" href="/about"> {email} </a><br/>
          <a id="Transaction History" className="menu-item" href="/about"> {currentBalance} </a><br/>
          <a id="Transaction History" className="menu-item" href="/about"> {address} </a>
        </Menu>
      </div>

    );
  }
};


// export default withStyles(styles, { withTheme: true })(Menus);
export default Menus


