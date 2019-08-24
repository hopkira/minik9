import React from 'react';
import user from './svg/user.svg';

class OnlineOrOff extends React.Component {
  state = {
    online:false
  }
  toggleImage = () => {this.setState(state => ({ online: !state.online}))
  }

  getImageColor = () => this.state.online ? '#24a148':'#da1e28'

render() {
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
          <img src={user} alt="listening" style={logoStyle} /> 
      </button>
    </div>
  </div>
  );
  }
}
export default OnlineOrOff