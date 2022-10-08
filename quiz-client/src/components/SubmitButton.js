export default function SubmitButton({text}){
    return (
        <button 
            type="submit" 
            class="py-3 w-64 text-xl text-white bg-sky-400 rounded-2xl">
                {text}
        </button>
    )
}