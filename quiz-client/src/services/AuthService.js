import axios from 'axios';

const base_url = process.env.REACT_APP_API_URI

export const login = async (username, password) => {
    const url = base_url+'auth/login/';

    try {
        const response = await axios.post(url,{
            username,
            password
        });
        return { response, isError: false };
    } catch (response) {
        return { response, isError: true };
    }
  };