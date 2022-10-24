function setLocalToken(token_value) {
    localStorage.setItem("access_token", token_value);
}

function getLocalToken() {
    return localStorage.getItem("access_token", null);
}

function isAuthenticated() {
    return localStorage.getItem("access_token", null) != null;
}

function removeLocalToken() {
    localStorage.removeItem("access_token");
}

export {setLocalToken, getLocalToken, isAuthenticated, removeLocalToken}