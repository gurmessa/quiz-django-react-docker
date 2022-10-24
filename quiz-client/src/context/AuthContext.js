import React, {createContext, useState} from "react";
import { setLocalToken, removeLocalToken, isAuthenticated } from "../utils/auth_utils";

export const AuthContext = createContext({
    isAuth: false, 
    authLogin: () => {}, 
    authLogout: () => {}
});


function AuthProvider({ children }) {
    const [isAuth, setIsAuth] = useState(isAuthenticated());
    
    const authLogin = (token) => {
      if(token) {
        setLocalToken(token);
        setIsAuth(true)
      }
    };
  
    const authLogout = () => {
        setIsAuth(false)
        removeLocalToken()
    };
  
    return (
      <AuthContext.Provider
        value={{
          isAuth: isAuth,
          authLogin,
          authLogout
        }}
      >
        {children}
      </AuthContext.Provider>
    );
  }
  
  export default AuthProvider;