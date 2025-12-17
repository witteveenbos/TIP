// Base types
export type Scenario = {
    id: string;
    name: string;
    description?: string;
    [key: string]: unknown;
};

export type AreaData = {
    id: string;
    name: string;
    level: Area;
    parentId?: string;
    [key: string]: unknown;
};

export type RegionHierarchy = {
    [regionId: string]: {
        id: string;
        name: string;
        level: Area;
        children?: string[];
        parent?: string;
        [key: string]: unknown;
    };
};

export type GeoMetadata = {
    bounds: [number, number, number, number];
    center: [number, number];
    zoom: number;
    [key: string]: unknown;
    legendLabels: [{
        [key: string]: string;
    }]
    legendTitle: string;
    unit: string;

};

export type GeoJSONFeature = {
    type: 'Feature';
    properties: {
        id: string;
        name: string;
        [key: string]: unknown;
    };
    geometry: {
        type: string;
        coordinates: number[] | number[][] | number[][][];
    };
};

export type GeoJSONData = {
    type: 'FeatureCollection';
    features: GeoJSONFeature[];
};

export type DevelopmentDefaults = {
    [municipalityId: string]: {
        [devKey: string]: {
            value: number;
            unit: string;
            [key: string]: unknown;
        };
    };
};

export type DevelopmentOptions = {
    [groupKey: string]: {
        name: string;
        developments: {
            [devKey: string]: {
                name: string;
                type: string;
                min: number;
                max: number;
                unit: string;
                [key: string]: unknown;
            };
        };
    };
};

export type CalculatedData = {
    [municipalityId: string]: {
        [indicator: string]: {
            value: number;
            unit: string;
            [key: string]: unknown;
        };
    };
};

export type SectoralProject = {
    id: string;
    name: string;
    municipalityId: string;
    [key: string]: unknown;
};

export interface ScenarioState {
    scenarios: Scenario[];
    setScenarios: (scenarios: Scenario[]) => void;
    selectedScenario: string | null;
    setSelectedScenario: (scenario: string) => void;
}

export interface AreaDivisionState {
    areaDivision: Array<{
        label: string;
        value: string;
    }>;
    setAreaDivision: (areaDivision: Array<{ label: string; value: string }>) => void;
    selectedAreaDivision: Area;
    setSelectedAreaDivision: (selectedAreaDivision: Area) => void;
}

export enum Area {
    PROV = 'PROV',
    REG = 'REG',
    GM = 'GM',
    RES = 'RES',
    HSMS = 'HSMS',
}

export interface MunicipalityScenariosState {
    municipalityScenarios: MunicipalityScenario[];
    setMunicipalityScenarios: (
        municipalityScenarios: MunicipalityScenario[]
    ) => void;
}

export type MunicipalityScenario = {
    ETMscenarioID: number;
    municipalityID: string;
};

export interface AllAreasState {
    allAreas: Record<string, AreaData>;
    setAllAreas: (allAreas: Record<string, AreaData>) => void;
}

export interface RegionHierarchyState {
    regionHierarchy: RegionHierarchy;
    regionHierarchyData: RegionHierarchy;
    setRegionHierarchy: (regionHierarchy: RegionHierarchy) => void;
}
export interface GeoJsonDataState {
    geoJsonData: {
        metadata: GeoMetadata | null;
        geoJSON: GeoJSONData | null;
    };
    setGeoJsonData: (geoJsonData: { metadata: GeoMetadata | null; geoJSON: GeoJSONData | null }) => void;
}

export interface SelectedGeoIDState {
    selectedGeoId: string | null;
    setSelectedGeoId: (selectedGeoId: string) => void;
}

export interface InputTypeState {
    inputType: 'continuous' | 'sectoral';
    setInputType: (inputType: 'continuous' | 'sectoral') => void;
}
export interface SelectedDevelopmentState {
    selectedDevelopment: {
        name: string;
        key: string;
        type: string;
        min: number;
        max: number;
        unit: string;
    } | null;
    setSelectedDevelopment: (selectedDevelopment: {
        name: string;
        key: string;
        type: string;
        min: number;
        max: number;
        unit: string;
    } | null) => void;
}

export type changedDevelopment = {
    projectId?: string;
    municipalityID: string;
    devGroupKey: string;
    changes: [
        {
            devKey: string;
            value: number;
        },
    ];
};

export interface ContinuousDevelopmentsChangesState {
    continuousDevelopmentDefaults: DevelopmentDefaults | null;
    setContinuousDevelopmentDefaults: (continuousDevelopmentDefaults: DevelopmentDefaults) => void;
    changedContinuousDevelopments: changedDevelopment[];
    setChangedContinuousDevelopments: (
        changedContinuousDevelopments: changedDevelopment[]
    ) => void;
}

export interface SectoralDevelopmentsChangesState {
    sectoralDevelopmentDefaults: DevelopmentDefaults | null;
    setSectoralDevelopmentDefaults: (sectoralDevelopmentDefaults: DevelopmentDefaults) => void;
    sectoralDevelopmentDefaultProjects: SectoralProject[];
    setSectoralDevelopmentDefaultProjects: (
        sectoralDevelopmentDefaultProjects: SectoralProject[]
    ) => void;
    changedSectoralDevelopments: changedDevelopment[];
    setChangedSectoralDevelopments: (changedSectoralDevelopments: changedDevelopment[]) => void;
}

// Additional interfaces for the store
export interface ContinuousOptionsState {
    continuousOptions: DevelopmentOptions;
    setContinuousOptions: (continuousOptions: DevelopmentOptions) => void;
}

export interface SectoralOptionsState {
    sectoralOptions: DevelopmentOptions;
    setSectoralOptions: (sectoralOptions: DevelopmentOptions) => void;
}

export interface CalculatedDataState {
    calculatedData: CalculatedData;
    setCalculatedData: (calculatedData: CalculatedData) => void;
}