import React from "react";
import Chessboard from "chessboardjsx";

class K9ChessBoard extends React.Component {
  render()
  {
    var board = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    if (this.props.isLoaded){
        board = this.props.position.toString();
        console.log(board)
    }
      return (
        <Chessboard
        id="standard"
        orientation="white"
        width={240}
        position={board}
        boardStyle={{
          borderRadius: "0px",
        }}
        dropOffBoard="trash"
        sparePieces={false}
        showNotation={true}
        draggable={false}
        lightSquareStyle={{ backgroundColor: "#ffffff" }}
        darkSquareStyle={{ backgroundColor: "#3d70b2" }}
      />
      );
    }
}
export default K9ChessBoard;