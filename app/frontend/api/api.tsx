import { PostUserInputRequest } from 'types/api/postUserInput';

const API_URL = process.env.NEXT_PUBLIC_API_URL;
const REKENKERN_API_URL = process.env.NEXT_PUBLIC_REKENKERN_API_URL;
const MOCK_RESPONSE_API = process.env.MOCK_RESPONSE_API;

type MunicipalityScenario = {
    ETMscenarioID: number;
    municipalityID: string;
};

export interface CalculateInterface {
    areaDivision?: string;
    mapType?: string;
    inputType?: string;
    scenario: string;
    municipalityScenarios: MunicipalityScenario[];
    continuousDevelopments: [];
    sectoralDevelopments: [];
}

export interface FutureVisionSelectionInterface {
    name: string;
    scenario: string;
    geo_id: string;
    REG01?: number;
    REG02?: number;
    REG03?: number;
    REG04?: number;
    REG05?: number;
    REG06?: number;
}

interface getMunicipalityScenariosInterface {
    dataLink: string;
}

export async function getScenarios() {
    const response = await fetch(`${REKENKERN_API_URL}/list_scenarios/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    return response.json();
}

export async function getMunicipalityScenarios(
    body: getMunicipalityScenariosInterface
) {
    const response = await fetch(
        `${REKENKERN_API_URL}/create_municipality_scenarios/`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        }
    );
    return response.json();
}

export async function getMainGraph(mainScenario: string) {
    const response = await fetch(
        `${REKENKERN_API_URL}/get_main_graph/?main_scenario=${encodeURIComponent(mainScenario)}`,
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }
    );
    return response.json();
}

export async function postUserInputs(body: PostUserInputRequest) {
    let queryString = '';
    if (MOCK_RESPONSE_API === 'true') {
        queryString = '?mock_response=true';
    }

    try {
        const response = await fetch(
            `${REKENKERN_API_URL}/post_user_values${queryString}/`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body),
            }
        );

        if (!response.ok) {
            return null;
        }

        return response.json();
    } catch (error) {
        console.error('Error posting user inputs:', error);

        return null;
    }
}

export async function getAreaDivisionOptions() {
    const response = await fetch(`${API_URL}/energy/options/area_division/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    return response.json();
}

export async function getGeoJSONs() {
    const response = await fetch(`${API_URL}/energy/geojsons/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    return response.json();
}

export async function getFutureVisions() {
    const response = await fetch(`${API_URL}/future-visions/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    return response.json();
}

export async function getFutureVision(futureVisionId) {
    const response = await fetch(
        `${API_URL}/future-visions/${futureVisionId}`,
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }
    );
    return response.json();
}

export async function putFutureVision(futureVision) {
    const response = await fetch(
        `${API_URL}/future-visions/${futureVision.id}/`,
        {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(futureVision),
        }
    );
    return response.json();
}

export async function postFutureVision(futureVision) {
    const response = await fetch(`${API_URL}/future-visions/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(futureVision),
    });
    return response.json();
}

export async function combineFutureVisions(
    futureVisionSelection: FutureVisionSelectionInterface
) {
    const response = await fetch(`${API_URL}/future-visions/combine/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(futureVisionSelection),
    });
    return response.json();
}

export async function getRegionHierarchy() {
    const response = await fetch(`${API_URL}/energy/options/region/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    return response.json();
}

export async function getResHierarchy() {
    const response = await fetch(`${API_URL}/energy/options/res/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    return response.json();
}
