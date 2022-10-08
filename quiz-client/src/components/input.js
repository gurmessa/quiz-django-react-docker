export default function Input({
    onChange,
    value, 
    error,
    type='text',
    placeholder,
    name
}){

    return <>
        <input 
            type={type} 
            placeholder={placeholder} 
            name={name}
            onChange={onChange}
            value={value}
            className={
                (error? "border-red-400 ":"") + "block text-sm py-3 px-4 rounded-lg w-full border outline-none"
            }
        />
        <span className="text-red-400 text-xs">{error}</span>

    </>

}