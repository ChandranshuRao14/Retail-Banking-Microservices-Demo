import React from "react";
import { Link } from "react-router-dom";

/* Style Sheet */
import "../styles/navbar.css";

/* TODO: Function to change id name of selected tab*/

const Navbar: React.FC = () => {
  return (
    <nav className="Navbar">
      <div className="Nav-link" id="Selected">
        <Link to="/">Home</Link>
      </div>
      <div className="Nav-link">
        <Link to="/profile">Profile</Link>
      </div>
      <div className="Nav-link">
        <Link to="/transfer">Transfer</Link>
      </div>
    </nav>
  );
};

export default Navbar;
