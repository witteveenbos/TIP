import { create } from 'zustand';
import { createJSONStorage, devtools, persist } from 'zustand/middleware';

interface ScenarioState {
    scenarios: [];
    setScenarios: (scenarios: any) => void;
    selectedScenario: string | null;
    setSelectedScenario: (scenario: string) => void;
}

interface AreaDivisionState {
    areaDivision:
        | string
        | Array<{
              label: string;
              value: string;
          }>;
    setAreaDivision: (areaDivision: string) => void;
    selectedAreaDivision: Area;
    setSelectedAreaDivision: (selectedAreaDivision: Area) => void;
}

enum Area {
    PROV = 'PROV',
    REG = 'REG',
    GM = 'GM',
    RES = 'RES',
}

interface MunicipalityScenariosState {
    municipalityScenarios: MunicipalityScenario[];
    setMunicipalityScenarios: (
        municipalityScenarios: MunicipalityScenario[]
    ) => void;
}

type MunicipalityScenario = {
    ETMscenarioID: number;
    municipalityID: string;
};

interface AllAreasState {
    allAreas: any;
    setAllAreas: (allAreas: any) => void;
}

interface RegionHierarchyState {
    regionHierarchy: any;
    regionHierarchyData: any;
    setRegionHierarchy: (regionHierarchy: any) => void;
}
interface GeoJsonDataState {
    geoJsonData: {
        metadata: any;
        geoJSON: any;
    };
    setGeoJsonData: (geoJsonData: any) => void;
}

interface SelectedGeoIDState {
    selectedGeoId: string | null;
    setSelectedGeoId: (selectedGeoId: string) => void;
}

interface inputTypeState {
    inputType: 'continuous' | 'sectoral';
    setInputType: (inputType) => void;
}
interface selectedDevelopmentState {
    selectedDevelopment: {
        name: string;
        key: string;
        type: string;
        min: number;
        max: number;
        unit: string;
    } | null;
    setSelectedDevelopment: (selectedDevelopment) => void;
}

type changedDevelopment = {
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

interface ContinuousDevelopmentsChangesState {
    continuousDevelopmentDefaults: {};
    setContinuousDevelopmentDefaults: (continuousDevelopmentDefaults: {}) => void;
    changedContinuousDevelopments: [];
    setChangedContinuousDevelopments: (
        changedContinuousDevelopments: changedDevelopment[]
    ) => void;
}

interface SectoralDevelopmentsChangesState {
    sectoralDevelopmentDefaults: {};
    setSectoralDevelopmentDefaults: (sectoralDevelopmentDefaults: {}) => void;
    sectoralDevelopmentDefaultProjects: [];
    setSectoralDevelopmentDefaultProjects: (
        sectoralDevelopmentDefaultProjects: []
    ) => void;
    changedSectoralDevelopments: changedDevelopment[];
    setChangedSectoralDevelopments: (changedSectoralDevelopments) => void;
}

export const useScenarioStore = create<ScenarioState>()(
    devtools(
        persist(
            (set) => ({
                scenarios: [],
                setScenarios: (scenarios: any) => set({ scenarios }),
                selectedScenario: null,
                setSelectedScenario: (selectedScenario: string) =>
                    set({ selectedScenario }),
            }),
            {
                name: 'scenario-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);

export const useAreaDivisionStore = create<AreaDivisionState>()(
    devtools(
        persist(
            (set) => ({
                areaDivision: '',
                setAreaDivision: (areaDivision: Area) => set({ areaDivision }),
                selectedAreaDivision: Area.GM,
                setSelectedAreaDivision: (selectedAreaDivision: Area) =>
                    set({ selectedAreaDivision }),
            }),
            {
                name: 'area-division-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);

export const useMunicipalityScenariosStore =
    create<MunicipalityScenariosState>()(
        devtools(
            persist(
                (set) => ({
                    municipalityScenarios: [],
                    setMunicipalityScenarios: (
                        municipalityScenarios: MunicipalityScenario[]
                    ) => set({ municipalityScenarios }),
                }),
                {
                    name: 'municipality-scenarios-store',
                    storage: createJSONStorage(() => sessionStorage),
                }
            )
        )
    );

export const useRegionHierarchyStore = create<RegionHierarchyState>()(
    devtools(
        persist(
            (set) => ({
                regionHierarchy: {},
                setRegionHierarchy: (regionHierarchyData: any) =>
                    set({ regionHierarchyData }),
            }),
            {
                name: 'region-hierarchy-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);

export const useAllAreasStore = create<AllAreasState>()(
    devtools(
        persist(
            (set) => ({
                allAreas: {},
                setAllAreas: (allAreas: any) => set({ allAreas }),
            }),
            {
                name: 'all-areas-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);

export const useGeoJsonDataStore = create<GeoJsonDataState>()(
    devtools(
        persist(
            (set) => ({
                geoJsonData: { metadata: null, geoJSON: null },
                setGeoJsonData: (geoJsonData: any) => set({ geoJsonData }),
            }),
            {
                name: 'geo-data-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);

export const useSelectedGeoIdStore = create<SelectedGeoIDState>()(
    devtools(
        persist(
            (set) => ({
                selectedGeoId: '',
                setSelectedGeoId: (selectedGeoId: string) =>
                    set({ selectedGeoId }),
            }),
            {
                name: 'geo-id-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);

export const useInputTypeStore = create<inputTypeState>()(
    devtools(
        persist(
            (set) => ({
                inputType: 'continuous',
                setInputType: (inputType) => set({ inputType }),
            }),
            {
                name: 'input-type-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);

export const selectedDevelopmentStore = create<selectedDevelopmentState>()(
    devtools(
        persist(
            (set) => ({
                selectedDevelopment: null,
                setSelectedDevelopment: (selectedDevelopment) =>
                    set({ selectedDevelopment }),
            }),
            {
                name: 'selected-development-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);

export const continuousDevelopmentsChangesStore =
    create<ContinuousDevelopmentsChangesState>()(
        devtools(
            persist(
                (set) => ({
                    continuousDevelopmentDefaults: null,
                    setContinuousDevelopmentDefaults: (
                        continuousDevelopmentDefaults
                    ) => set({ continuousDevelopmentDefaults }),

                    changedContinuousDevelopments: [],
                    setChangedContinuousDevelopments: (
                        changedContinuousDevelopments: []
                    ) => set({ changedContinuousDevelopments }),
                }),
                {
                    name: 'continuous-developments-changes-store',
                    storage: createJSONStorage(() => sessionStorage),
                }
            )
        )
    );
export const sectoralDevelopmentsChangesStore = create()(
    devtools(
        persist(
            (set) => ({
                sectoralDevelopmentDefaults: null,
                setSectoralDevelopmentDefaults: (sectoralDevelopmentDefaults) =>
                    set({ sectoralDevelopmentDefaults }),
                sectoralDevelopmentDefaultProjects: [],
                setSectoralDevelopmentDefaultProjects: (
                    sectoralDevelopmentDefaultProjects: []
                ) => set({ sectoralDevelopmentDefaultProjects }),

                changedSectoralDevelopments: [],
                setChangedSectoralDevelopments: (
                    changedSectoralDevelopments: []
                ) => set({ changedSectoralDevelopments }),
            }),
            {
                name: 'sectoral-developments-changes-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);

export const useContinuousOptionsStore = create()(
    devtools(
        persist(
            (set) => ({
                continuousOptions: {},
                setContinuousOptions: (continuousOptions: any) =>
                    set({ continuousOptions }),
            }),
            {
                name: 'continuous-options-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);

export const useSectoralOptionsStore = create()(
    devtools(
        persist(
            (set) => ({
                sectoralOptions: {},
                setSectoralOptions: (sectoralOptions: any) =>
                    set({ sectoralOptions }),
            }),
            {
                name: 'sectorial-options-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);

export const useCalculatedDataStore = create()(
    devtools(
        persist(
            (set) => ({
                calculatedData: {},
                setCalculatedData: (calculatedData: any) =>
                    set({ calculatedData }),
            }),
            {
                name: 'calculated-data-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);
