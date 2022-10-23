
function SearchQuizzes({searchTerm, setSearchTerm}){

    const handleChange = (e) => {
      setSearchTerm(e.target.value)
    }


    return (<>
    <label for="default-search" class="bg-white text-sm font-medium text-gray-900 sr-only ">Search</label>
    <div class="relative">
        <div class="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none">
            <svg aria-hidden="true" class="w-4 h-4 text-gray-500 " fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
        </div>
        <input 
            onChange={handleChange}
            type="search" 
            class="block p-3 pl-10 w-full text-sm text-gray-900 bg-white rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 " 
            placeholder="Search Quizzes" 
            value={searchTerm}
            />
     
    </div>

    </>)
}

export default SearchQuizzes;
