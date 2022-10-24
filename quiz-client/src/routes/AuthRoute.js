import { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext} from '../context/AuthContext';

const AuthRoute = ({ children }) => {
    const { isAuth } = useContext(AuthContext);

    if (isAuth) {
      return <Navigate to="/"  />;
    }

    return children;
  };

export default AuthRoute