import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom'
import './App.css';
import './index.js';
import Settings from './pages/settings';
import Chess from './pages/chess';
import Slack from './pages/slack';
import ToDo from './pages/todo';
import Home from './pages/home';


class App extends React.Component {
  state = {
    githubURL: "https://github.ibm.com/api/v3",
    gitToken: "5d48b5c18e1bb2212f1e9369a0dc241aa14885e6",
    gitUser: "richard-hopkins",
    gitRepo: "488186"
  }
  /*
  componentDidMount() {
    
    fetch('/api/issues',{
      method: 'GET',
    })
    .then(res => res.json())
    .then((todos) => {
      this.setState({todos});
      console.log(this.state.todos);
    })
    .catch(console.log)
  } 
  */
  render() { 
    return (
      <Router>
        <Switch>
          <Route path="/todo" component={ToDo}/>
          <Route path="/chess" component={Chess}/>
          <Route path="/settings" component={Settings}/>
          <Route path="/slack" component={Slack}/>
          <Route path="/" component={Home}/>
        </Switch>
    </Router>
    );
  }
}

export default App;
