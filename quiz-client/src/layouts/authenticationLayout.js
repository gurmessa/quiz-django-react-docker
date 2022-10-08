function AuthenticationLayout({children}){
    return (
<div class="min-h-screen max-h-screen bg-sky-400 flex justify-center items-center">
	<div class="absolute w-60 h-60 rounded-xl bg-sky-300 -top-5 -left-16 z-0 transform rotate-45 hidden md:block">
	</div>
	<div class="absolute w-48 h-48 rounded-xl bg-sky-300 -bottom-6 -right-10 transform rotate-12 hidden md:block">
	</div>
	<div class="py-12 px-12 bg-white rounded-2xl shadow-xl z-20">
        { children }
		</div>
		<div class="w-40 h-40 absolute bg-sky-300 rounded-full top-0 right-12 hidden md:block"></div>
		<div
			class="w-20 h-40 absolute bg-sky-300 rounded-full bottom-20 left-10 transform rotate-45 hidden md:block">
		</div>
	</div>

    )
    
} 


export default AuthenticationLayout;