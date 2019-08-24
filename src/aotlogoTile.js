import React from 'react';
import aot_logo from './graphics/chessboard.png';

const logoStyle = {
    width: '80px',
    height: '80px',
    background: '#3d70b2',
    fill: 'white',
    verticalAlign: 'middle',
    padding: '10px 30px'
  };

const buttonStyle = {
    height: '100px',
    width: '140px',
    background: '#ffffff',
    padding: '10px 10px',
    display: 'inline-block',
    marginLeft: 'auto',
    marginRight: 'auto'
  };

function AoTLogo(){
    return (
    <div>
    <div className="quarter-div center-div">
        <div style={buttonStyle}>
            <img src={aot_logo} alt="aot logo" style={logoStyle} /> 
        </div>
    </div>
    </div>
    );
}
export default AoTLogo;