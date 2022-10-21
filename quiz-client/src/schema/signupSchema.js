import * as Yup from 'yup';

const yupSignupValidation = Yup.object().shape({
  username: Yup.string().required("Username is required"),
  email: Yup.string().email().required("Email is required"),
  password1: Yup.string().required("Password is required").min(8, 'Your password is too short.'),
  password2: Yup.string().required("Confirm Password is required").test('passwords-match', 'Passwords must match', function(value){
    return this.parent.password1 === value
  }),
});


export  {yupSignupValidation }