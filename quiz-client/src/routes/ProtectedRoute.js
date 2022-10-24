import { useContext } from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import { AuthContext} from '../context/AuthContext';
import { getLocalToken } from '../utils/auth_utils';

const ProtectedRoute = ({ children }) => {
    const { isAuth } = useContext(AuthContext);

    if (!isAuth) {
      return <Navigate to="/login"  />;
    }

    return children;
  };

export default ProtectedRoute