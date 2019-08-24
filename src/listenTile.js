import React from 'react';
import listen_on from './svg/awake.svg';
import listen_off from './svg/asleep.svg';

class AsleepOrAwake extends React.Component {
  constructor(props) {
    super(props);
    // Define your state object here
    this.state = {
        listening: JSON.parse(localStorage.getItem('listening'))
      }
  }
  toggleImage = () => {this.setState(state => ({ listening: !state.listening}));}

  getImageName = () => JSON.parse(localStorage.getItem('listening')) ? listen_on:listen_off
  getImageColor = () => JSON.parse(localStorage.getItem('listening')) ? '#24a148':'#da1e28'

  render() {
    localStorage.setItem('listening',this.state.listening)
    const imageName = this.getImageName();
    const imageColor = this.getImageColor();
    const buttonStyle = {
      height: '100px',
      width: '140px',
      background: imageColor,
      padding: '0px 30px',
      display: 'inline-block',
    };
    const logoStyle = {
      width: '80px',
      height: '80px',
      background: imageColor,
      verticalAlign: 'middle',
      float: 'left'
    };
    return(
      <div>
      <div className="quarter-div center-div">
        <button style={buttonStyle} onClick={this.toggleImage}>
            <img src={imageName} alt="listening" style={logoStyle} /> 
        </button>
      </div>
    </div>
    );
  }
}
export default AsleepOrAwake