import React from 'react';
import done_logo from './svg/todo.svg';

const logoStyle = {
    width: '80px',
    height: '80px',
    background: '#24a148',
    fill: 'white',
    verticalAlign: 'middle',
    float: 'left'
  };

const buttonStyle = {
    height: '100px',
    width: '140px',
    background: '#24a148',
    padding: '0px 30px',
    display: 'inline-block',
  };

function DoneLogo(){
    return (
    <div>
    <div className="quarter-div center-div">
        <button style={buttonStyle}>
            <img src={done_logo} alt="done logo" style={logoStyle} /> 
        </button>
    </div>
    </div>
    );
}
export default DoneLogo;