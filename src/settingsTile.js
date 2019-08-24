import React from 'react';
import settings_logo from './svg/settings.svg';

const logoStyle = {
    width: '80px',
    height: '80px',
    background: '#3d70b2',
    fill: 'white',
    verticalAlign: 'middle',
    float: 'left'
  };

const buttonStyle = {
    height: '100px',
    width: '140px',
    background: '#3d70b2',
    padding: '0px 30px',
    display: 'inline-block',
  };

function SettingsLogo(){
    return (
    <div>
    <div className="quarter-div center-div">
        <button style={buttonStyle}>
            <img src={settings_logo} alt="settings logo" style={logoStyle} /> 
        </button>
    </div>
    </div>
    );
}
export default SettingsLogo;