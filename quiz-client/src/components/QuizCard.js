export default function QuizCard({quiz}){
    const handleClick = () =>{
        console.log(quiz.id)
    }

    return (
    <div className="w-1/2 sm:w-1/3">
        <div className="rounded-2xl shadow-lg bg-white m-1 sm:m-2">
        {/*<img class="w-full" src="/img/card-top.jpg" alt="Sunset in the mountains">*/}
            <div class="px-6 py-4">
                <div class="font-semibold text-xl sm:text-2xl">{quiz.title}</div>
                <span class="inline-block text-sm base:text-base font-light text-gray-700 tracking-wide">{quiz.category}</span>
        
                {/*<p class="text-gray-600 text-base mt-2">
                    {quiz.description}
                </p>*/}
            </div>
            <div class="px-6 pt-2 pb-2">
                <div className="my-1 text-sm sm:text-base px-1 sm:px-2  py-1">
                    {quiz.taken?
                    <>
                    {quiz.has_passed?
                        <span class="text-green-600 ">✅Passed </span>
                        :
                        <span class="text-red-400">❌Didn't Pass</span>
                    }
                    </>
                    :
                    <span 
                        onClick={handleClick}
                        class=" cursor-pointer text-sky-400 hover:bg-gray-100 rounded-md px-2 py-2">
                        Take Quiz
                    </span>
                    }
                </div>
            </div>
        </div>
    </div>
    )
}