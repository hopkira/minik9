import React from 'react';
import todo_logo from './svg/list.svg';
import ZenHub from './zenhub';

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

 const circleStyle = {
    height: '30px',
    width: '30px',
    backgroundColor: 'white',
    padding: '0px 0px',
    textAlign: 'center',
    borderRadius: '50%',
    lineHeight: '30px',
    border: 'none',
    color: '#3d70b2',
    position: 'fixed',
    top: '28px',
    left: '34px',
    fontWeight: '700',
    fontSize: '100%'
}

function ToDoLogo(){
    return (
    <div>
    <div className="quarter-div center-div">
        <button style={buttonStyle}>
            <img src={todo_logo} alt="to do logo" style={logoStyle} /> 
            <div style={circleStyle}><ZenHub /></div>
        </button>
    </div>
    </div>
    );
}
export default ToDoLogo;