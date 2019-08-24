import React from 'react';

class ZenHub extends React.Component {
    render() {
        var number = 0
        console.log(this.props.todos)
        if (this.props.isLoaded) {
            number = parseInt(this.props.todos.length);
            //console.log(number)
            //console.log(this.state.todos)
            }
        return (
            <div>
                {number}
            </div>
        );
    }
}
export default ZenHub;