import { useState } from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';
import { getLocalToken } from './utils/auth_utils';

function App() {

  const [isLoggedIn, setLoggedIn] = useState(Boolean(getLocalToken()));

  return (
    <div>
      <Routes>
        <Route path='/' element={<Home/>} />
        <Route path='/login' element={isLoggedIn ? <Navigate to='/' /> : <Login/>} />
      </Routes>
    </div>
  );
}

export default App;
