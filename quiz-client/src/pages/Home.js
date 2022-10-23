import { useState, useEffect } from "react"

import { getQuizzes, getCategories } from "../services/QuizSerivce"
import QuizCard from "../components/QuizCard";
import SearchQuizzes from "../components/SearchQuizzes";
import CategorySelector from "../components/CategorySelector";

const ALL_CATEGORY_ITEM = {title:"All", id:'all'}

export default function Home(){
    const [quizzes, setQuizzes] = useState([]);
    const [searchTerm, setSearchTerm] = useState([]);
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState(ALL_CATEGORY_ITEM)

    const loadQuizzes = async (term=null,category=null) => {
        setQuizzes([]);
        const { response, isError } = await getQuizzes(term,category);
        if (isError) {

        }else{
            setQuizzes(response.data)
        }

    }

    useEffect(()=>{
        loadQuizzes()
    }, [])

    useEffect(()=>{
        if(selectedCategory.id !== 'all'){
            loadQuizzes(searchTerm, selectedCategory.id)
        }else{
            loadQuizzes(searchTerm)
        }
        
    }, [selectedCategory, searchTerm])


    useEffect(()=>{
        const loadCategories = async () => {
            const { response, isError } = await getCategories();
            if (isError) {
    
            }else{
                setCategories([ALL_CATEGORY_ITEM, ...response.data])
            }
        }

        loadCategories()
    }, [])


    return (<div className="bg-gray-100 h-screen">
        <div className="max-w-5xl mx-auto">
            <h1 class="font-bold text-2xl sm:text-3xl py-5 px-3">Take Quizzes</h1>
            <div className="flex gap-2">
               <CategorySelector 
                    categories={categories}
                    selectedCategory={selectedCategory}
                    setSelectedCategory={setSelectedCategory}
                />
                <br />
                <br />
                <SearchQuizzes 
                    searchTerm={searchTerm}
                    setSearchTerm={setSearchTerm}/>
                </div>
            <div class="flex mx-auto flex-wrap mt-8">
                {quizzes.map(quiz => <QuizCard quiz={quiz} />)}
            </div>
        </div>



    </div>)
}