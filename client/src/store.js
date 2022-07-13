import { writable } from 'svelte/store';

export function getCookie(key) {
    let cookies = document.cookie.split('; ');
    let cookieKey = key + "=";
    let cookie = cookies.find((cookie) => cookie.indexOf(cookieKey) === 0)
    if (cookie) {
        return cookie.replace(cookieKey, '');
    }
    else {
        return undefined
    }
}

export function request(url, method = 'GET', body = null, accept = 'application/json', contentType = 'application/json') {
    const token = getCookie('token');
    const headers = {};
    headers.Authorization = `Bearer ${token ? token : ''}`;
    if (accept) {
        headers.Accept = accept;
    }
    if (contentType) {
        headers["Content-Type"] = contentType;
    }
    const options = {
        method,
        headers
    };
    if (body) {
        options.body = body;
    }

    return fetch(url, options).then((response) => {
        return response.ok ? response.json().then((json) => json.data) : null;
    });
}

export function getFile(url){
    const token = getCookie('token');
    const headers = {};
    const method = "GET";
    headers.Authorization = `Bearer ${token ? token : ''}`;
    const options = {
        method,
        headers
    };

    return fetch(url, options).then((response) => {
        return response.ok ? response.blob() : null;
    });
}

export function checkAuth() {
    const url = 'api/authcheck';
    const token = getCookie('token');
    const options = {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token ? token : ''}`
        },
    };

    return fetch(url, options).then((response) => {
        return { auth: response.ok };
    }).catch(() => {
        return { auth: false };
    });
}

export function getUser() {
    const url = "/api/user";
    return request(url);
}

export function getGroups() {
    const url = "/api/groups";
    return request(url);
}