import React from 'react'
import {Link} from 'react-router-dom';
import CircleTileSlack from '../circleTileSlack';
import MenuLogo from '../menuTile';
import OnlineOrOff from '../userTile';
import TextTile from '../textTile';


function Slack() {
    return (
        <div className="App">
            <div id="top_left" className="quarter-div center-div">
                <CircleTileSlack />
            </div>
            <div>
                <TextTile />
            </div>
            <div id="bottom_left" className="quarter-div center-div">
                <Link to='/'>
                    <MenuLogo />
                </Link>
            </div>
            <div id="bottom_right" className="quarter-div center-div">
                <OnlineOrOff />
            </div>
        </div>
    )
}

export default Slack