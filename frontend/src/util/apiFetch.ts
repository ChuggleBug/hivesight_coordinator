
// A wrapper for fetch which handles hostname
export default function apiFetchCloud(input: string | URL | globalThis.Request, init?: RequestInit) {
    return fetch(`http://localhost:3000${input}`, init);
}

export function apiFetchCoordinator(input: string | URL | globalThis.Request, init?: RequestInit) {
    return fetch(`http://localhost:3030${input}`, init);
}