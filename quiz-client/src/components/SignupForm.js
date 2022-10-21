import { useState } from 'react';
import { Login, Navigate } from 'react-router-dom';
import { Formik, ErrorMessage } from 'formik';
import Input from './Input';
import SubmitButton from './SubmitButton';
import Warning from './Warning.js';
import { yupSignupValidation } from '../schema/signupSchema';
import { signup } from '../services/AuthService';


export default function SignupForm(){
    const [error, setError] = useState(false)
    const [success, setSuccess] = useState(false)
    
    const onSubmit = async(values, actions) => {
        setError(false)

        const { response, isError } = await signup(
            values.username, values.email, 
            values.password1, values.password2
        );
        if (isError) {
            const data = response.response.data;
            for (const value in data) {
                actions.setFieldError(value, data[value].join(' '));
            }
            
            setError(true)
        }else{
            setSuccess(true)
        }

    }

    if (success) {
        return <Navigate to='/login' />
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
            validationSchema={yupSignupValidation}
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
                                name="email"
                                placeholder="Email"
                                value={values.email}
                                error={errors.email}
                                onChange={handleChange}
                                type="email"
                            />
                            <Input 
                                name="password1"
                                placeholder="Password"
                                value={values.password1}
                                error={errors.password1}
                                onChange={handleChange}
                                type="password"
                            />
                            <Input 
                                name="password2"
                                placeholder="Confirm Password"
                                value={values.password2}
                                error={errors.password2}
                                onChange={handleChange}
                                type="password"
                            />
                        </div>
                        <div class="text-center mt-6">
                            <SubmitButton 
                                text="Create Account"
                            />
                            <p class="mt-4 text-sm">Already Have An Account? <span class="underline cursor-pointer"> Sign In</span>
                            </p>
                        </div>
                    </form>
                </>
            )
            }

        </Formik>
    </>
}