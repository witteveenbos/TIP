import { ArrowUturnLeftIcon } from '@heroicons/react/24/outline';
import { RadioGroup } from '@radix-ui/react-radio-group';
import { useEffect, useState } from 'react';
import {
    continuousDevelopmentsChangesStore,
    sectoralDevelopmentsChangesStore,
    selectedDevelopmentStore,
    useAreaDivisionStore,
    useMunicipalityScenariosStore,
    useScenarioStore,
} from 'stores/calculateStore';
import { useDragersStore } from 'stores/headerTogglesStore';
import { Switch } from '../ui/switch';
import Development from './Development';
import s from './EnergyBalance.module.css';

export default function ContinuousDevelopments({
    gid,
    developments,
    allExpandedRows,
}) {
    const [inputWarning, setInputWarning] = useState('');
    const { changedContinuousDevelopments, setChangedContinuousDevelopments } =
        continuousDevelopmentsChangesStore();
    const { changedSectoralDevelopments } = sectoralDevelopmentsChangesStore();
    const { selectedDevelopment, setSelectedDevelopment } =
        selectedDevelopmentStore();
    const { selectedAreaDivision } = useAreaDivisionStore();
    const { selectedScenario } = useScenarioStore();
    const { municipalityScenarios } = useMunicipalityScenariosStore();
    const { original, setOriginal } = useDragersStore();

    useEffect(() => {
        setInputWarning('');
    }, [selectedDevelopment]);

    function saveInput(event) {
        setInputWarning('');
        //if header is set to original - set to aangepast
        original && setOriginal(false);

        let inputvalue = parseFloat(event.target.value);

        if (inputvalue < parseFloat(event.target.min)) {
            inputvalue = event.target.min;
        }
        if (inputvalue > parseFloat(event.target.max)) {
            inputvalue = event.target.max;
        }

        const existingDevelopmentIndex =
            changedContinuousDevelopments.findIndex(
                (cd) =>
                    cd.municipalityID === gid &&
                    cd.devGroupKey === selectedDevelopment.key
            );

        if (existingDevelopmentIndex > -1) {
            const updatedDevelopments = [...changedContinuousDevelopments];
            const existingDevelopment =
                updatedDevelopments[existingDevelopmentIndex];

            existingDevelopment.changes = existingDevelopment.changes.map(
                (change) => {
                    if (
                        change.devKey ===
                        event.target.getAttribute('data-develop-input')
                    ) {
                        return {
                            ...change,
                            devKey: change.devKey,
                            value: inputvalue,
                        };
                    } else {
                        return change;
                    }
                }
            );

            updatedDevelopments[existingDevelopmentIndex] = existingDevelopment;
            setChangedContinuousDevelopments(updatedDevelopments);

            if (
                existingDevelopment.devGroupKey ===
                    'verduurzaming_utiliteiten' ||
                existingDevelopment.devGroupKey ===
                    'verduurzaming_bestaande_bouw'
            ) {
                checkTotalValue(existingDevelopment);
            }
        } else {
            const devInputOptions = developments.filter(
                (dev) =>
                    dev.type === 'continuous' &&
                    dev.key === selectedDevelopment.key
            )[0].inputs;
            const newChangedContinuousDevelopment = {
                devGroupKey: selectedDevelopment.key,
                municipalityID: gid,
                changes: devInputOptions.map((option) => {
                    if (
                        option.key ===
                        event.target.getAttribute('data-develop-input')
                    ) {
                        return {
                            devKey: option.key,
                            value: inputvalue,
                            default: option.default,
                        };
                    } else {
                        return {
                            devKey: option.key,
                            value: option.default,
                            default: option.default,
                        };
                    }
                }),
            };

            setChangedContinuousDevelopments([
                ...changedContinuousDevelopments,
                newChangedContinuousDevelopment,
            ]);

            if (
                newChangedContinuousDevelopment.devGroupKey ===
                    'verduurzaming_utiliteiten' ||
                newChangedContinuousDevelopment.devGroupKey ===
                    'verduurzaming_bestaande_bouw'
            ) {
                checkTotalValue(newChangedContinuousDevelopment);
            }
        }
    }

    function resetValue(developmentId) {
        const updatedDevelopments = changedContinuousDevelopments.filter(
            (cd) =>
                cd.municipalityID !== gid || cd.devGroupKey !== developmentId
        );
        setChangedContinuousDevelopments(updatedDevelopments);
    }

    function checkTotalValue(development) {
        const totalDefaultValue = Math.ceil(
            development.changes.reduce(
                (sum, input) => sum + parseFloat(input.default),
                0
            )
        );

        const totalCurrentValue = Math.ceil(
            development.changes.reduce(
                (sum, input) => sum + parseFloat(input.value),
                0
            )
        );
        if (totalCurrentValue !== totalDefaultValue) {
            setInputWarning(
                `Let op: je hebt ${totalCurrentValue} units geconfigureerd maar er zijn ${totalDefaultValue} units in totaal.`
            );
        } else {
            setInputWarning('');
        }
    }

    function toggleOrSetActiveID(id) {
        if (selectedDevelopment && selectedDevelopment.key === id) {
            setSelectedDevelopment(null);
        } else {
            const development = developments.find(
                (development) => development.key === id
            );
            if (!development) return;
            setSelectedDevelopment({
                key: id,
                type: 'cd',
                name: development.name,
                min: development.inputs[0].min,
                max: development.inputs[0].max,
                unit: development.inputs[0].unit,
            });
        }
    }

    return (
        <RadioGroup className="flex flex-col flex-1 overflow-y-auto">
            <div className={`flex items-center flex-col justify-between gap-2`}>
                {developments &&
                    developments.length > 0 &&
                    developments.map((development: any, index: any) => {
                        const developmentKey = development.value
                            ? development.value
                            : development.key;
                        return (
                            <div
                                key={index}
                                className={` ${s.ButtonWithSwitch} ${developmentKey == selectedDevelopment?.key && s.ButtonWithSwitch__active} bg-white cursor-pointer p-1 border-2 border-transparent w-[95%] justify-between text-primary h-auto hover:text-white group gap-2`}>
                                <>
                                    <div
                                        onClick={() => {
                                            toggleOrSetActiveID(developmentKey);
                                        }}
                                        className={`${s.ButtonWithSwitch__summary}`}>
                                        <small
                                            className={` ${developmentKey == selectedDevelopment?.key ? 'text-white ' : undefined} ${s.ButtonWithSwitch__label} truncate`}>
                                            {development.name ||
                                                development.label}
                                        </small>
                                        <div>
                                            <small
                                                className={
                                                    developmentKey ==
                                                    selectedDevelopment?.key
                                                        ? 'text-white '
                                                        : undefined
                                                }>
                                                {development.unit}
                                            </small>
                                        </div>

                                        <Switch
                                            className="pointer-events-none"
                                            checked={
                                                developmentKey ==
                                                selectedDevelopment?.key
                                            }
                                        />
                                    </div>

                                    {allExpandedRows &&
                                        selectedDevelopment?.key ===
                                            developmentKey && (
                                            <div
                                                className={`${s.ButtonWithSwitch__details}`}>
                                                <div className="flex flex-col gap-1 w-full">
                                                    {development.inputs.map(
                                                        (
                                                            developmentInput,
                                                            index
                                                        ) => (
                                                            <Development
                                                                key={index}
                                                                gid={gid}
                                                                saveInput={
                                                                    saveInput
                                                                }
                                                                developmentInput={
                                                                    developmentInput
                                                                }
                                                                developmentKey={
                                                                    developmentKey
                                                                }
                                                                developmentType="continuous"
                                                                changedDevelopments={
                                                                    changedContinuousDevelopments
                                                                }
                                                                selectedDevelopment={
                                                                    selectedDevelopment
                                                                }
                                                                selectedAreaDivision={
                                                                    selectedAreaDivision
                                                                }></Development>
                                                        )
                                                    )}
                                                    {inputWarning && (
                                                        <div className="text-white text-sm">
                                                            {inputWarning}
                                                        </div>
                                                    )}
                                                </div>

                                                {changedContinuousDevelopments.find(
                                                    (cd: any) =>
                                                        cd.municipalityID ===
                                                            gid &&
                                                        cd.devGroupKey ===
                                                            development.key
                                                ) && (
                                                    <span
                                                        onClick={(e) => {
                                                            e.stopPropagation();
                                                            resetValue(
                                                                development.key
                                                            );
                                                        }}
                                                        className={`${s.ButtonWithSwitch__details__right}`}>
                                                        <ArrowUturnLeftIcon className="h-4 w-4" />
                                                    </span>
                                                )}
                                            </div>
                                        )}
                                </>
                            </div>
                        );
                    })}
            </div>
        </RadioGroup>
    );
}
