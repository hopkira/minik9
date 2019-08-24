import React, {Component} from 'react';
import K9ChessBoard from './k9chessboard';

class ChessScreen extends Component{
  render() {
    return (
      <div style={boardsContainer}>
        <K9ChessBoard />
      </div>
    );
}
}
export default ChessScreen;

const boardsContainer = {
  display: "flex",
  justifyContent: "space-around",
  alignItems: "center",
  flexWrap: "wrap",
  width: "240",
  marginTop: 0,
  marginBottom: 50,
  background: "3d70b2"
};