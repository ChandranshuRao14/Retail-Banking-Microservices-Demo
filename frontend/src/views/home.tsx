import React from "react";
import AccountBalance from "../components/HomeBalance";
import Transfer from "../components/HomeTransfer";
import Transactions from "../components/HomeTransactions";

const Home: React.FC = () => {
  return ( 
      <div style={container}>
        <div style={item}><AccountBalance></AccountBalance></div>
        <div style={item}><Transactions></Transactions></div>
        <div style={item}><Transfer></Transfer></div>
      </div>
  );
};

const container={
  display: "grid", 
  gridTemplateColumns: "repeat(3, 1fr)", 
  gridTemplateRows: '70vh',
  gridGap: 20,
  marginTop: '40px',
}

const item={
  backgroundColor: '#4285F4',
  color: '#fff',
  border: '1px solid #fff',
  margin: '20px',
  padding: '20px',
  fontSize: '15px',
  borderRadius: '10px',
  height: '100%'
}

export default Home;
