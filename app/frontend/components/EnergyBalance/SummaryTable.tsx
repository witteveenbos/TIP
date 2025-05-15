import { useEffect, useState } from 'react';
import {
    getRegionHierarchy,
    getResHierarchy,
    postUserInputs,
} from '../../api/api';

import {
    continuousDevelopmentsChangesStore,
    sectoralDevelopmentsChangesStore,
    useAllAreasStore,
    useAreaDivisionStore,
    useInputTypeStore,
    useMunicipalityScenariosStore,
    useRegionHierarchyStore,
} from 'stores/calculateStore';
import { useDragersStore } from 'stores/headerTogglesStore';

export default function SummaryTable({ gid, developmentkey }) {
    const { allAreas } = useAllAreasStore(); // Get all areas from store
    const { inputType, setInputType } = useInputTypeStore();
    const { setAreaDivision, selectedAreaDivision } = useAreaDivisionStore();
    const { regionHierarchyData, setRegionHierarchy } =
        useRegionHierarchyStore();
    const { changedContinuousDevelopments, setChangedContinuousDevelopments } =
        continuousDevelopmentsChangesStore();
    const { changedSectoralDevelopments, setChangedSectoralDevelopments } =
        sectoralDevelopmentsChangesStore();
    const { municipalityScenarios } = useMunicipalityScenariosStore();
    const { energyCarrier, balance, original } = useDragersStore();

    const [defaults, setDefaults] = useState(null);

    const development =
        inputType === 'sectoral'
            ? {
                  sectoral_developments: changedSectoralDevelopments,
              }
            : {
                  continuous_developments: changedContinuousDevelopments,
              };

    function getDefaults(areadivision) {
        const postData = {
            viewSettings: {
                areaDivision: areadivision,
                energyCarrier: energyCarrier,
                balance: balance,
                original: original,
                developmentType: inputType,
                graphType: null,
            },
            userSettings: {
                municipalityScenarios: municipalityScenarios,
                continuousDevelopments: changedContinuousDevelopments,
                sectoralDevelopments: changedSectoralDevelopments,
            },
        };
        console.log('summaryTable');
        postUserInputs(postData).then((res) => {
            setDefaults(res.input);
        });
    }

    useEffect(() => {
        if (selectedAreaDivision == 'RES') {
            getDefaults('GM');
            getResHierarchy().then((res) => {
                if (res) {
                    setRegionHierarchy(res);
                }
            });
        } else if (selectedAreaDivision == 'REG') {
            getDefaults('GM');
            getRegionHierarchy().then((res) => {
                if (res) {
                    setRegionHierarchy(res);
                }
            });
        } else {
            //prov
            getRegionHierarchy().then((res) => {
                getDefaults('REG');
                if (res) {
                    setRegionHierarchy(res);
                }
            });
        }
    }, [selectedAreaDivision]);

    return (
        <table className="text-sm">
            <thead>
                <tr>
                    {/* {Object.keys(data.array[0]).map((item,index)=><th key={index}>{item}</th>)} */}
                </tr>
            </thead>
            <tbody>
                {selectedAreaDivision == 'PROV' ? (
                    <>
                        <p>{defaults?.length}</p>
                        {defaults &&
                            Object.keys(defaults)?.map((item, index) => (
                                <tr key={index}>
                                    <td key={index}>
                                        <span>
                                            {
                                                allAreas['REG'].find(
                                                    (gm) => gm.gid == item
                                                )?.label
                                            }
                                        </span>
                                    </td>
                                    <td className="text-right">
                                        <span>
                                            {Math.round(
                                                defaults[item][0].default
                                            )}
                                        </span>
                                    </td>
                                </tr>
                            ))}
                    </>
                ) : (
                    <>
                        {defaults &&
                            Object.keys(defaults)
                                ?.filter((defaultItem) =>
                                    regionHierarchyData[gid]?.includes(
                                        defaultItem
                                    )
                                )
                                ?.map((item, index) => (
                                    <tr key={index}>
                                        <td>
                                            <span>
                                                {
                                                    allAreas['GM'].find(
                                                        (gm) => gm.gid == item
                                                    )?.label
                                                }
                                            </span>
                                        </td>
                                        <>
                                            {inputType === 'sectoral' ? (
                                                <>
                                                    {changedSectoralDevelopments.filter(
                                                        (cd) =>
                                                            cd.gid == item &&
                                                            cd.development ==
                                                                developmentkey
                                                    ).length ? (
                                                        <td
                                                            className={`text-right`}>
                                                            <span>
                                                                {changedSectoralDevelopments
                                                                    .filter(
                                                                        (sd) =>
                                                                            sd.gid ==
                                                                                item &&
                                                                            sd.development ==
                                                                                developmentkey
                                                                    )
                                                                    ?.map(
                                                                        (dev) =>
                                                                            dev.inputs
                                                                    )
                                                                    .flat()
                                                                    .reduce(
                                                                        (
                                                                            innerAcc,
                                                                            innerObj
                                                                        ) => {
                                                                            return (
                                                                                parseFloat(
                                                                                    innerAcc
                                                                                ) +
                                                                                parseFloat(
                                                                                    innerObj.value
                                                                                )
                                                                            );
                                                                        },
                                                                        0
                                                                    )}
                                                            </span>
                                                        </td>
                                                    ) : (
                                                        defaults[item]
                                                            .find(
                                                                (item) =>
                                                                    item.key ==
                                                                    developmentkey
                                                            )
                                                            ?.inputs?.map(
                                                                (
                                                                    input,
                                                                    index
                                                                ) => (
                                                                    <td
                                                                        className="text-right"
                                                                        key={
                                                                            index
                                                                        }>
                                                                        <span>
                                                                            {Math.round(
                                                                                input.default
                                                                            )}
                                                                        </span>
                                                                    </td>
                                                                )
                                                            )
                                                    )}
                                                </>
                                            ) : (
                                                <>
                                                    {changedContinuousDevelopments.find(
                                                        (cd) =>
                                                            cd.gid == item &&
                                                            cd.development ==
                                                                developmentkey
                                                    ) ? (
                                                        <>
                                                            {changedContinuousDevelopments
                                                                .find(
                                                                    (cd) =>
                                                                        cd.gid ==
                                                                            item &&
                                                                        cd.development ==
                                                                            developmentkey
                                                                )
                                                                ?.inputs.map(
                                                                    (
                                                                        input,
                                                                        index
                                                                    ) => (
                                                                        <td
                                                                            className="text-right"
                                                                            key={
                                                                                index
                                                                            }>
                                                                            <span>
                                                                                <strong>
                                                                                    {Math.round(
                                                                                        input.value
                                                                                    )}
                                                                                </strong>
                                                                            </span>
                                                                        </td>
                                                                    )
                                                                )}
                                                        </>
                                                    ) : (
                                                        <>
                                                            {defaults[item]
                                                                .find(
                                                                    (item) =>
                                                                        item.key ==
                                                                        developmentkey
                                                                )
                                                                .inputs.map(
                                                                    (
                                                                        input,
                                                                        index
                                                                    ) => (
                                                                        <td
                                                                            className="text-right"
                                                                            key={
                                                                                index
                                                                            }>
                                                                            <span>
                                                                                {Math.round(
                                                                                    input.default
                                                                                )}
                                                                            </span>
                                                                        </td>
                                                                    )
                                                                )}
                                                        </>
                                                    )}
                                                </>
                                            )}
                                        </>
                                    </tr>
                                ))}
                    </>
                )}
            </tbody>
        </table>
    );
}
