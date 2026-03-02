import { create } from 'zustand';
import { createJSONStorage, devtools, persist } from 'zustand/middleware';
import {
    Area,
    AreaData,
    AreaDivisionState,
    AllAreasState,
    CalculatedData,
    CalculatedDataState,
    changedDevelopment,
    ContinuousDevelopmentsChangesState,
    ContinuousOptionsState,
    DevelopmentDefaults,
    DevelopmentOptions,
    GeoJSONData,
    GeoJsonDataState,
    GeoMetadata,
    InputTypeState,
    MunicipalityScenario,
    MunicipalityScenariosState,
    RegionHierarchy,
    RegionHierarchyState,
    Scenario,
    ScenarioState,
    SectoralDevelopmentsChangesState,
    SectoralOptionsState,
    SectoralProject,
    SelectedDevelopmentState,
    SelectedGeoIDState,
} from '@/types/stores/calculateStore';



export const useScenarioStore = create<ScenarioState>()(
    devtools(
        persist(
            (set) => ({
                scenarios: [],
                setScenarios: (scenarios: Scenario[]) => set({ scenarios }),
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
                areaDivision: [],
                setAreaDivision: (areaDivision: Array<{ label: string; value: string }>) => set({ areaDivision }),
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
                regionHierarchyData: {},
                setRegionHierarchy: (regionHierarchyData: RegionHierarchy) =>
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
                setAllAreas: (allAreas: Record<string, AreaData>) => set({ allAreas }),
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
                setGeoJsonData: (geoJsonData: { metadata: GeoMetadata | null; geoJSON: GeoJSONData | null }) => set({ geoJsonData }),
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

export const useInputTypeStore = create<InputTypeState>()(
    devtools(
        persist(
            (set) => ({
                inputType: 'continuous',
                setInputType: (inputType: 'continuous' | 'sectoral') => set({ inputType }),
            }),
            {
                name: 'input-type-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);

export const selectedDevelopmentStore = create<SelectedDevelopmentState>()(
    devtools(
        persist(
            (set) => ({
                selectedDevelopment: null,
                setSelectedDevelopment: (selectedDevelopment: {
                    name: string;
                    key: string;
                    type: string;
                    min: number;
                    max: number;
                    unit: string;
                } | null) =>
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
                        continuousDevelopmentDefaults: DevelopmentDefaults
                    ) => set({ continuousDevelopmentDefaults }),

                    changedContinuousDevelopments: [],
                    setChangedContinuousDevelopments: (
                        changedContinuousDevelopments: changedDevelopment[]
                    ) => set({ changedContinuousDevelopments }),
                }),
                {
                    name: 'continuous-developments-changes-store',
                    storage: createJSONStorage(() => sessionStorage),
                }
            )
        )
    );


export const sectoralDevelopmentsChangesStore = create<SectoralDevelopmentsChangesState>()(
    devtools(
        persist(
            (set) => ({
                sectoralDevelopmentDefaults: null,
                setSectoralDevelopmentDefaults: (sectoralDevelopmentDefaults: DevelopmentDefaults) =>
                    set({ sectoralDevelopmentDefaults }),
                sectoralDevelopmentDefaultProjects: [],
                setSectoralDevelopmentDefaultProjects: (
                    sectoralDevelopmentDefaultProjects: SectoralProject[]
                ) => set({ sectoralDevelopmentDefaultProjects }),

                changedSectoralDevelopments: [],
                setChangedSectoralDevelopments: (
                    changedSectoralDevelopments: changedDevelopment[]
                ) => set({ changedSectoralDevelopments }),
            }),
            {
                name: 'sectoral-developments-changes-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);

export const useContinuousOptionsStore = create<ContinuousOptionsState>()(
    devtools(
        persist(
            (set) => ({
                continuousOptions: {},
                setContinuousOptions: (continuousOptions: DevelopmentOptions) =>
                    set({ continuousOptions }),
            }),
            {
                name: 'continuous-options-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);

export const useSectoralOptionsStore = create<SectoralOptionsState>()(
    devtools(
        persist(
            (set) => ({
                sectoralOptions: {},
                setSectoralOptions: (sectoralOptions: DevelopmentOptions) =>
                    set({ sectoralOptions }),
            }),
            {
                name: 'sectorial-options-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);

export const useCalculatedDataStore = create<CalculatedDataState>()(
    devtools(
        persist(
            (set) => ({
                calculatedData: {},
                setCalculatedData: (calculatedData: CalculatedData) =>
                    set({ calculatedData }),
            }),
            {
                name: 'calculated-data-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);
