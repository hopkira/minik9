import React from 'react';
import {Link} from 'react-router-dom';
import ToDoLogo from '../todoTile';
import MessagesLogo from '../messageTile';
import AoTLogo from '../aotlogoTile';
import SettingsLogo from '../settingsTile';

function Home() {
    return (
        <div className="App">
        <div id="top_left" className="quarter-div center-div">
        <Link to='/todo'>
            <ToDoLogo />
        </Link>
        </div>
        <div>
        <Link to='/settings'>
            <SettingsLogo />
        </Link>
        </div>
        <div id="bottom_left" className="quarter-div center-div">
        <Link to='/chess'>
            <AoTLogo />
        </Link>
        </div>
        <div id="bottom_right" className="quarter-div center-div">
            <Link to='/slack'>
                <MessagesLogo />
            </Link>
        </div>
    </div>
    )
}
export default Home