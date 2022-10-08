export default function Warning({text}){
    return (
        <div class="p-4 mb-4 text-sm text-gray-700 bg-gray-100 rounded-lg dark:bg-gray-200 dark:text-gray-800" role="alert">
            <span class="font-medium">
                {text}
            </span>  
        </div>   
    )
}