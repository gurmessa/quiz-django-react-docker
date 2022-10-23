import axios from 'axios';
import { getLocalToken } from '../utils/auth_utils';

const base_url = process.env.REACT_APP_API_URI

export const getQuizzes = async (term=null,category=null) => {
    let url = base_url+'quizzes';
    if(term || category){
        url += '?';

        if(term){
            url += `&title=${term}`
        }
        if(category){
            url += `&category=${category}`
        }
    }

    const token = getLocalToken()
    const headers = { Authorization: `Token ${token}` };

    try {
        const response = await axios.get(url, { headers });
        return { response, isError: false };
    } catch (response) {
        return { response, isError: true };
    }
  };


  export const getCategories = async () => {
    let url = base_url+'categories';
    
    try {
        const response = await axios.get(url, );
        return { response, isError: false };
    } catch (response) {
        return { response, isError: true };
    }
  };
