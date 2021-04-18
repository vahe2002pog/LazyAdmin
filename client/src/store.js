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

function request(url, method = 'GET', body = null) {
    const token = getCookie('token');
    const options = {
        method,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token ? token : ''}`
        }
    };
    if (body) {
        options.body = JSON.stringify(body);
    }

    return fetch(url, options).then((response) => {
        return response.ok ? response.json().then((json) => json.data) : null;
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

export function getUser(){
    const url = "/api/user";
    return request(url);
}

export function getGroups(){
    const url = "/api/groups";
    return request(url);
}