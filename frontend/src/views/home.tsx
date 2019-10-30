import React from "react";
import HomeDetails from "../components/home-details";
import HomeAccounts from "../components/home-accounts";
import "../styles/home.css";

const Home: React.FC = () => {
  return (
    <div className="Home-Container">
      <div className="Home-Container-Top">
        <div>
          <h2>Home</h2>
        </div>
      </div>
      <div className="Home-Container-Bottom">
        <div className="Home-Container-Left">
          <HomeAccounts></HomeAccounts>
        </div>
        <div className="Home-Container-Right">
          <HomeDetails></HomeDetails>
        </div>
      </div>
    </div>
  );
};

export default Home;
