import React from "react";
import {makeStyles, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper} from '@material-ui/core';


const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

function createData(id: string, amount: number, type: string, date: string, balance: number) {
  return { id, amount, type, date, balance };
}

const rows = [
  createData('Frozen yoghurt', 159, "credit", "2019/2/4", 4.0),
  createData('Ice cream sandwich', 237, "dedit", "2019/2/4", 4.3),
  createData('Eclair', 262, "credit", "2019/2/4", 6.0),
  createData('Cupcake', 305, "dedit", "2019/2/4", 4.3),
  createData('Gingerbread1', 356, "credit", "2019/2/4", 3.9),
  createData('Cupcake1', 305, "dedit", "2019/2/4", 4.3),
  createData('Gingerbread1', 356, "credit", "2019/2/4", 3.9),
  createData('Frozen yoghurt2', 159, "credit", "2019/2/4", 4.0),
  createData('Ice cream sandwich2', 237, "dedit", "2019/2/4", 4.3),
  createData('Eclair2', 262, "credit", "2019/2/4", 6.0),
  createData('Cupcake2', 305, "dedit", "2019/2/4", 4.3),
  createData('Gingerbread2', 356, "credit", "2019/2/4", 3.9),
  createData('Frozen yoghurt3', 159, "credit", "2019/2/4", 4.0),
  createData('Ice cream sandwich3', 237, "dedit", "2019/2/4", 4.3),
  createData('Eclair3', 262, "credit", "2019/2/4", 6.0),
  createData('Cupcake3', 305, "dedit", "2019/2/4", 4.3),
  createData('Gingerbread3', 356, "credit", "2019/2/4", 3.9),
  createData('Frozen yoghurt4', 159, "credit", "2019/2/4", 4.0),
  createData('Ice cream sandwich4', 237, "dedit", "2019/2/4", 4.3),
  createData('Eclair4', 262, "credit", "2019/2/4", 6.0),
  createData('Cupcake4', 305, "dedit", "2019/2/4", 4.3),
  createData('Gingerbread4', 356, "credit", "2019/2/4", 3.9),
  createData('Frozen yoghurt5', 159, "credit", "2019/2/4", 4.0),
  createData('Ice cream sandwich5', 237, "dedit", "2019/2/4", 4.3),
  createData('Eclair5', 262, "credit", "2019/2/4", 6.0),
  createData('Cupcake5', 305, "dedit", "2019/2/4", 4.3),
  createData('Gingerbread5', 356, "credit", "2019/2/4", 3.9),
];

const Transactions: React.FC = () => {
  const classes = useStyles();
  return (
    <div>
      <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="simple table">
        <TableHead>
          <TableRow>
              <TableCell>Transaction ID</TableCell>
              <TableCell align="right">Amount</TableCell>
              <TableCell align="right">Type</TableCell>
              <TableCell align="right">Date</TableCell>
              <TableCell align="right">Ended Balance</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map(row => (
              <TableRow key={row.id}>
                <TableCell component="th" scope="row">
                  {row.id}
                </TableCell>
                <TableCell align="right">{row.amount}</TableCell>
                <TableCell align="right">{row.type}</TableCell>
                <TableCell align="right">{row.date}</TableCell>
                <TableCell align="right">{row.balance}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default Transactions;




