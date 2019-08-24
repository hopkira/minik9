import React from 'react';
import {Link} from 'react-router-dom';
import K9ChessBoard from '../k9chessboard';

class Chess extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            position: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
            isLoaded: false
        };
      } 
    componentDidMount(){
        this.ticker = setInterval(
            () => this.tick(), 100);
        }

    componentWillUnmount(){
        clearInterval(this.ticker)
    }

    tick = () => {
        fetch('/api/readboard',{
            method: 'GET',
        })
        .then((response)=>{
            return response.text();
            //this.setState({
            //    position: data,
            //    isLoaded: true});
        })
        .then((text)=>{
            var FENstring;
            FENstring = text.toString()
            console.log(FENstring);
            this.setState({
                position: FENstring,
                isLoaded: true
            });

        })
    }

    render()
    {
    return (
        <div className="App">
                <Link to='/home'>
                    <div style={boardsContainer}>
                    <K9ChessBoard position = {this.state.position} isLoaded = {this.state.isLoaded}/>
                    </div>
                </Link>
        </div>
        )
    }
}
export default Chess

const boardsContainer = {
    display: "flex",
    justifyContent: "space-around",
    alignItems: "center",
    flexWrap: "wrap",
    width: "240",
    marginTop: 0,
    marginBottom: 0,
    background: "#3d70b2"
  };