import React from 'react';
import ZenHub from './zenhub';

class CircleTileZen extends React.Component {
    render() {
        return (
        <div className="button circle-button">      
            <ZenHub todos = {this.props.todos} isLoaded = {this.props.isLoaded} />
        </div>
        );
    }
}
export default CircleTileZen;