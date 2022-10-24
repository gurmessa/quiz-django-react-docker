import { useState, useContext } from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import AuthProvider from './context/AuthContext';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Home from './pages/Home';
import ProtectedRoute from './routes/ProtectedRoute';
import AuthRoute from './routes/AuthRoute';

function App() {

  return (
    <AuthProvider>
      <Routes>
        <Route 
          path='/' 
          element={
            <ProtectedRoute>
              <Home/>
            </ProtectedRoute>
          }
        >
        </Route>
        <Route 
          path='/login' 
          element={
            <AuthRoute>
              <Login/>
            </AuthRoute>
          } 
        />
        <Route 
          path='/signup' 
          element={
            <AuthRoute>
              <Signup/>
            </AuthRoute>
          }
        />
      </Routes> 
      </AuthProvider>
  );
}

export default App;
