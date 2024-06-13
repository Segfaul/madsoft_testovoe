import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

import Home from './components/Home';
import PrivateMemes from './components/meme/PrivateMeme';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="App">
        <h1>Meme App</h1>
        <a href='http://127.0.0.1:8000/api/swagger' target='_blank'>Public API</a>
        <a href='http://127.0.0.1:8001/api/swagger' target='_blank'>Private API</a>
        <div className="nav-menu">
          <Link to={'/private'}>Move to Private module</Link>
          <Link to={'/'}>Move to Public module</Link>
        </div>
        <Routes>
          <Route path='/' element={<Home />}/>
          <Route path='/private' element={<PrivateMemes />}/>
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;
