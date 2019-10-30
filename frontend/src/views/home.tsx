import React from "react";
import HomeDetails from "../components/home-details";
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
          <h1>Left Side</h1>
        </div>
        <div className="Home-Container-Right">
          <h1>Right Side</h1>
          <HomeDetails></HomeDetails>
        </div>
      </div>
    </div>
  );
};

export default Home;
