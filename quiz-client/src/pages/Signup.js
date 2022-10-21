import AuthenticationLayout from "../layouts/authenticationLayout";
import SignupForm from "../components/SignupForm";

function Signup(){
    return <>

        <AuthenticationLayout>
            <div>
                <h1 class="text-3xl font-bold text-center mb-4 cursor-pointer">Create An Account</h1>
                <p class="w-80 text-center text-sm mb-8 font-semibold text-gray-700 tracking-wide cursor-pointer"></p>
            </div>
            <SignupForm/>
        </AuthenticationLayout>
    </>
} 


export default Signup;