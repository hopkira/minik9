import React from 'react'
import {Link} from 'react-router-dom';
import CircleTileZen from '../circleTileZen';
import MenuLogo from '../menuTile';
import DoneLogo from '../completeTile';
import TextTile from '../textTile';

class ToDo extends React.Component {
        constructor(props) {
            super(props);
            this.state = {
                isLoaded: false,
                todos: null
            };
          }
    componentDidMount() {     
    fetch('/api/issues',{
        method: 'GET',
        })
        .then(res => res.json())
        .then((todos) => {
        this.setState({
            todos,
            isLoaded: true
        });
        console.log(this.state.todos);
        })
        .catch(console.log)
    }
    render()
        {
        return (
            <div className="App">
                <div id="top_left" className="quarter-div center-div">
                    <CircleTileZen todos = {this.state.todos} isLoaded = {this.state.isLoaded}/>
                </div>
                <div>
                    <TextTile todos = {this.state.todos} isLoaded = {this.state.isLoaded}/>
                </div>
                <div id="bottom_left" className="quarter-div center-div">
                    <Link to='/'>
                        <MenuLogo />
                    </Link>
                </div>
                <div id="bottom_right" className="quarter-div center-div">
                    <DoneLogo todos = {this.state.todos} isLoaded = {this.state.isLoaded}/>
                </div>
            </div>
        )
    }
}
export default ToDo