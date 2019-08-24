import React from 'react';
import user from './svg/power.svg';

class OnOrOff extends React.Component {
  constructor(props) {
    super(props);
    // Define your state object here
    this.state = {
        on: JSON.parse(localStorage.getItem('on'))
      }
    //console.log("init: "+JSON.parse(localStorage.getItem('on')),this.state.on)
  }
  toggleImage = () => {
    //console.log("before - store:"+JSON.parse(localStorage.getItem('on'))+" state:"+this.state.on)
    this.setState(state => ({ on: !state.on}));
    //console.log("after - store:"+JSON.parse(localStorage.getItem('on'))+" state:"+this.state.on)
  }

  getImageColor = () => JSON.parse(localStorage.getItem('on')) ? '#24a148':'#da1e28'

  render() {
    localStorage.setItem('on',this.state.on)
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
            <img src={user} alt="power" style={logoStyle} /> 
        </button>
      </div>
    </div>
    );
    }
}
export default OnOrOff