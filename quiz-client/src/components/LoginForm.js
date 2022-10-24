import { useState, useContext } from 'react';
import { Login, Navigate } from 'react-router-dom';
import { Formik, ErrorMessage } from 'formik';
import Input from './Input';
import SubmitButton from '../components/SubmitButton';
import Warning from './Warning.js';
import { yupLoginValidation } from '../schema/loginSchema';
import { login } from '../services/AuthService';
import { setLocalToken } from '../utils/auth_utils';
import { AuthContext } from '../context/AuthContext';

export default function LoginForm(){
    const [error, setError] = useState(false)
    const [success, setSuccess] = useState(false)
    const { authLogin } = useContext(AuthContext)
    
    const onSubmit = async(values, actions) => {
        setError(false)

        const { response, isError } = await login(values.username, values.password);
        if (isError) {
            const data = response;
            setError(true)
        }else{
            authLogin(response.data['key']);
            //setLocalToken(response.data['key']);
            setSuccess(true)
        }

    }

    if (success) {
        return <Navigate to='/' />
    }
    
    return <>
        { error?
        <Warning 
            text="Please enter a correct email address and password"
        />:''
        }


        <Formik
            initialValues={{
                username: '',
                password: ''
            }}
            onSubmit={onSubmit}
            validationSchema={yupLoginValidation}
            validateOnChange={false}
            validateOnBlur={false}
        >
            {({
                errors,
                handleChange,
                handleSubmit,
                isSubmitting,
                values
            }) => (
                <>
                    <form noValidate onSubmit={handleSubmit}>
                        <div class="space-y-4">
                            <Input 
                                name="username"
                                placeholder="Username"
                                value={values.username}
                                error={errors.username}
                                onChange={handleChange}
                            />
                            <Input 
                                name="password"
                                placeholder="Password"
                                value={values.password}
                                error={errors.password}
                                onChange={handleChange}
                            />
                        </div>
                        <div class="text-center mt-6">
                            <SubmitButton 
                                text="Login"
                            />
                            <p class="mt-4 text-sm pt-0">Don't have an account? <span class="underline cursor-pointer">Sign Up</span>
                            </p>
                        </div>
                    </form>
                </>
            )
            }

        </Formik>
    </>
}