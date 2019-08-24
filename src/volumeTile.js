import React from 'react';
import silent from './svg/notification-off.svg';
import noisy from './svg/notification-on.svg';

class SilentOrNoisy extends React.Component {
  constructor(props) {
    super(props);
    // Define your state object here
    this.state = {
        volume: JSON.parse(localStorage.getItem('volume'))
      }
  }
  toggleImage = () => {this.setState(state => ({ volume: !state.volume}))}

  getImageName = () => JSON.parse(localStorage.getItem('volume')) ? noisy:silent
  getImageColor = () => JSON.parse(localStorage.getItem('volume')) ? '#24a148':'#da1e28'

render() {
  localStorage.setItem('volume',this.state.volume)
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
          <img src={imageName} alt="volume" style={logoStyle} /> 
      </button>
    </div>
  </div>
  );
  }
}
export default SilentOrNoisy