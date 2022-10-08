import AuthenticationLayout from "../layouts/authenticationLayout";

function Login(){
    return <>

        <AuthenticationLayout>
            <div>
                <h1 class="text-3xl font-bold text-center mb-4 cursor-pointer">Create An Account</h1>
                <p class="w-80 text-center text-sm mb-8 font-semibold text-gray-700 tracking-wide cursor-pointer">Create an
                    account to enjoy all the services without any ads for free!</p>
            </div>
            <div class="space-y-4">
                <input type="text" placeholder="Email Addres" class="block text-sm py-3 px-4 rounded-lg w-full border outline-none" />
                <input type="text" placeholder="Password" class="block text-sm py-3 px-4 rounded-lg w-full border outline-none" />
            </div>
            <div class="text-center mt-6">
                <button class="py-3 w-64 text-xl text-white bg-sky-400 rounded-2xl">Create Account</button>
                <p class="mt-4 text-sm">Already Have An Account? <span class="underline cursor-pointer"> Sign In</span>
                </p>
            </div>
        </AuthenticationLayout>
    </>
} 


export default Login;