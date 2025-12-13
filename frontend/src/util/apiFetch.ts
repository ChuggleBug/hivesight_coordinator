
export const CLOUD_HOST = "http://ec2-34-238-248-180.compute-1.amazonaws.com"
export const COORDINATOR_HOST = "http://localhost:3030"

// A wrapper for fetch which handles hostname
export default function apiFetchCloud(input: string | URL | globalThis.Request, init?: RequestInit) {
    return fetch(`${CLOUD_HOST}${input}`, init);
}

export function apiFetchCoordinator(input: string | URL | globalThis.Request, init?: RequestInit) {
    return fetch(`${COORDINATOR_HOST}${input}`, init);
}