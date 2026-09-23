import type { Project, ProjectModification } from './Workboardpage';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

const getCsrfToken = () =>
    document.cookie
        .split('; ')
        .find((cookie) => cookie.startsWith('csrftoken='))
        ?.split('=')[1];

const requestHeaders = () => ({
    'Content-Type': 'application/json',
    'X-CSRFToken': getCsrfToken() || '',
});

const request = async (url: string, options: RequestInit = {}) => {
    const response = await fetch(`${API_URL}${url}`, {
        credentials: 'include',
        ...options,
        headers: {
            ...requestHeaders(),
            ...options.headers,
        },
    });

    if (!response.ok) {
        throw new Error(`Workboard request failed: ${response.status}`);
    }

    return response;
};

export const getProjects = (pageId: number) =>
    request(`/workboarditems/${pageId}/`).then(
        (response) => response.json() as Promise<Project[]>
    );

export const getModifications = (projectId: number) =>
    request(`/workboarditems/item/${projectId}/modifications/`).then(
        (response) => response.json() as Promise<ProjectModification[]>
    );

export const createProject = (
    pageId: number,
    project: Pick<
        Project,
        'title' | 'description' | 'type' | 'size_mw' | 'acm_prio' | 'status'
    >
) =>
    request(`/workboarditems/${pageId}/`, {
        method: 'POST',
        body: JSON.stringify(project),
    }).then((response) => response.json() as Promise<Project>);

export const updateProject = (
    projectId: number,
    project: Pick<
        Project,
        'title' | 'description' | 'type' | 'size_mw' | 'acm_prio' | 'status'
    >
) =>
    request(`/workboarditems/item/${projectId}/`, {
        method: 'PATCH',
        body: JSON.stringify(project),
    }).then((response) => response.json() as Promise<Project>);

export const deleteProject = (projectId: number) =>
    request(`/workboarditems/item/${projectId}/`, { method: 'DELETE' });

export const moveProject = (
    projectId: number,
    lane: number,
    targetProjectId?: number,
    insertBefore = false
) =>
    request(`/workboarditems/item/${projectId}/position/`, {
        method: 'PATCH',
        body: JSON.stringify({
            lane,
            target_item_id: targetProjectId ?? null,
            insert_before: insertBefore,
        }),
    });
