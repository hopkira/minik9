import React from 'react';

class TextTile extends React.Component{
    render() {
        var text = ""
        if (this.props.isLoaded){
            text = this.props.todos[0].title;
        }
        return (
        <div className="center-div center-div-text">      
            {text}
        </div>
        );
    }
}
export default TextTile;