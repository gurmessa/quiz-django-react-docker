import AuthenticationLayout from "../layouts/authenticationLayout";
import LoginForm from "../components/LoginForm";

function Login(){
    
    return (
        <AuthenticationLayout>
            <div>
                <h1 class="text-3xl font-bold text-center mb-4 cursor-pointer">Quiz App</h1>
                <p class="w-80 text-center text-sm mb-8 font-semibold text-gray-700 tracking-wide cursor-pointer">
                    Login to your account
                </p>
            </div>
            <LoginForm/>
        
         </AuthenticationLayout>
    )
} 


export default Login;