import React from "react";
import {Button, Modal, ButtonToolbar} from 'react-bootstrap'
import {makeStyles, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TextField} from '@material-ui/core';
import { Fab} from '@material-ui/core';
import AddIcon from '@material-ui/icons/Add';

const useStyles = makeStyles(theme => ({
  root: {
    '& .MuiTextField-root': {
      margin: theme.spacing(1),
      width: 200,
    },
  },
}));

function MyVerticallyCenteredModal(props) {
  const classes = useStyles();
  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          Make a Transaction
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
          <form className={classes.root} noValidate autoComplete="off">
            <div>
              <TextField required id="standard-required" label="From"/>
              <TextField required id="standard-required" label="To"/>
              <TextField required id="standard-required" label="Amount"/>
              <TextField id="standard-required" label="Note"/>
            </div>
          </form>
      </Modal.Body>
      <Modal.Footer>
        <Button onClick={props.onHide}>Submit</Button>
      </Modal.Footer>
    </Modal>
  );
}

const Transactions: React.FC = () => {
  const [modalShow, setModalShow] = React.useState(false);

  return (
    <div style={{position: 'relative', height: '100%'}}>
      <h1>Transactions</h1>
      <p>Transaction 1</p>
      <p>Transaction 2</p>
      <p>Transaction 3</p>
      <Fab color="primary" aria-label="add" style={{position: 'absolute', right: '0px',
                bottom: '0px'}}>
        <AddIcon onClick={() => setModalShow(true)}></AddIcon>
        <MyVerticallyCenteredModal
            show={modalShow}
            onHide={() => setModalShow(false)}
          />
      </Fab>
    </div>
  );
};

export default Transactions;