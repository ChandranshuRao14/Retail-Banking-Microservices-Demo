import React from 'react';
import {Container, Navbar, NavbarBrand } from 'reactstrap';

class TopBar extends React.Component {
  constructor(props: Readonly<{}>) {
    super(props);
  }

  render() {
    return (
      <Navbar color="dark" dark expand="md">
        <Container>
          <NavbarBrand href="/">
            <span>Oswaldo Díaz</span>
          </NavbarBrand>
        </Container>
      </Navbar>
    );
  }
}

export default TopBar;