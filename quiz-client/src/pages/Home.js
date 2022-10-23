import { useState, useEffect } from "react"
import { getQuizzes } from "../services/QuizSerivce"
import QuizCard from "../components/QuizCard";
import SearchComponent from "../components/SearchComponent";

export default function Home(){
    const [quizzes, setQuizzes] = useState([]);

    const loadQuizzes = async (term=null) => {
        setQuizzes([]);
        const { response, isError } = await getQuizzes(term);
        if (isError) {

        }else{
            setQuizzes(response.data)
        }

    }

    const handleTermChange = (term) => {
        loadQuizzes(term)
    }
    useEffect(()=>{
        loadQuizzes()
    }, [])

    return (<div className="bg-gray-100 h-screen">
        <div className="max-w-5xl mx-auto">
            <h1 class="font-bold text-2xl sm:text-3xl py-5 px-3">Take Quizzes</h1>
            <SearchComponent handleTermChange={handleTermChange}/>
            <div class="flex mx-auto flex-wrap">
                {quizzes.map(quiz => <QuizCard quiz={quiz} />)}
            </div>
        </div>
    </div>)
}