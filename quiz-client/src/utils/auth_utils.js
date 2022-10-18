function setLocalToken(token_value) {
    localStorage.setItem("access_token", token_value);
}

function getLocalToken() {
    return localStorage.getItem("access_token", null);
}


export {setLocalToken, getLocalToken}