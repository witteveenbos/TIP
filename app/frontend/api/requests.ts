import querystring from 'querystring';
import {
    keysToCamelFromSnake,
    keysToSnakeFromCamel,
} from '../utils/caseconverters';
import { getCookie } from '@/utils/cookie';

interface RequestOptions {
    headers?: Record<string, string>;
}
// Authentication requests may target the backend on a different origin.
const credentialsMode: RequestCredentials = 'include';

export async function getRequest(
    url: string,
    params: Record<string, any> = {},
    options: RequestOptions = {}
): Promise<any> {
    params = params || {};
    params = keysToSnakeFromCamel(params);
    const csrfToken = getCookie('csrftoken');

    let headers = options?.headers || {};
    headers = {
        'Content-Type': 'application/json',
        ...(csrfToken && { 'X-CSRFToken': csrfToken }),
        ...headers,
    };
    const queryString = querystring.stringify(params);

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000); // 30 second timeout

    try {
        const res = await fetch(`${url}?${queryString}`, {
            headers,
            signal: controller.signal,
            credentials: credentialsMode,
        });
        clearTimeout(timeout);

        if (res.status < 200 || res.status >= 300) {
            const error = new WagtailApiResponseError(res, url, params);
            throw error;
        }

        const json = await res.json();
        return {
            headers: res.headers,
            json: keysToCamelFromSnake(json),
        };
    } catch (error) {
        clearTimeout(timeout);
        if (error instanceof Error && error.name === 'AbortError') {
            throw new Error(`Request timeout after 30s: ${url}`);
        }
        throw error;
    }
}

export async function postRequest(
    url: string,
    params: Record<string, any> = {},
    options: RequestOptions = {}
): Promise<any> {
    params = params || {};
    params = keysToSnakeFromCamel(params);

    const csrfToken = getCookie('csrftoken');
    let headers = options?.headers || {};
    headers = {
        'Content-Type': 'application/json',
        ...(csrfToken && { 'X-CSRFToken': csrfToken }),
        ...headers,
    };

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000); // 30 second timeout

    try {
        const res = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(params),
            headers,
            credentials: credentialsMode,
            signal: controller.signal,
        });
        clearTimeout(timeout);

        if (res.status < 200 || res.status >= 300) {
            const error = new WagtailApiResponseError(res, url, params);
            throw error;
        }

        const json = await res.json();
        return {
            headers: res.headers,
            json: keysToCamelFromSnake(json),
        };
    } catch (error) {
        clearTimeout(timeout);
        if (error instanceof Error && error.name === 'AbortError') {
            throw new Error(`Request timeout after 30s: ${url}`);
        }
        throw error;
    }
}

export class WagtailApiResponseError extends Error {
    response;
    constructor(res: Response, url: any, params: any) {
        super(
            `${res.statusText}. Url: ${url}. Params: ${JSON.stringify(params)}`
        );
        this.name = 'WagtailApiResponseError';
        this.response = res;
    }
}
