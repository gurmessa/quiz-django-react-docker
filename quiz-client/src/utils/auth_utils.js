function setLocalToken(token_value) {
    localStorage.setItem("access_token", token_value);
}

function getLocalToken() {
    localStorage.getItem("access_token", '');
}


export {setLocalToken, getLocalToken}