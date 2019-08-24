import React from 'react'
import {Link} from 'react-router-dom';
import AsleepOrAwake from '../listenTile';
import MenuLogo from '../menuTile';
import OnOrOff from '../powerTile';
import SilentOrNoisy from '../volumeTile';


function Settings() {
    return (
        <div className="App">
            <div id="top_left" className="quarter-div center-div">
                <AsleepOrAwake />
            </div>
            <div>
                <SilentOrNoisy />
            </div>
            <div id="bottom_left" className="quarter-div center-div">
                <Link to='/'>
                    <MenuLogo />
                </Link>
            </div>
            <div id="bottom_right" className="quarter-div center-div">
                <OnOrOff />
            </div>
        </div>
    )
}

export default Settings