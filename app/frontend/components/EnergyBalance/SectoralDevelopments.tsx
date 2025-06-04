import {
    ChevronDownIcon,
    ChevronRightIcon,
    TrashIcon,
} from '@heroicons/react/24/outline';
import { RadioGroup } from '@radix-ui/react-radio-group';
import { useState } from 'react';
import {
    continuousDevelopmentsChangesStore,
    sectoralDevelopmentsChangesStore,
    selectedDevelopmentStore,
    useAreaDivisionStore,
} from 'stores/calculateStore';
import { useDragersStore } from 'stores/headerTogglesStore';
import { Button } from '../ui/button';
import { Switch } from '../ui/switch';
import Development from './Development';
import s from './EnergyBalance.module.css';
import SectoralNewProject from './SectoralNewProject';

export default function SectoralDevelopments({
    gid,
    developments,
    allExpandedRows,
    aggregatedProjects,
}) {
    const [expandedProjects, setExpandedProjects] = useState([]);
    const [newProjectOpen, setNewProjectOpen] = useState(false);
    const { changedContinuousDevelopments } =
        continuousDevelopmentsChangesStore();
    const {
        changedSectoralDevelopments,
        setChangedSectoralDevelopments,
        sectoralDevelopmentDefaultProjects,
    } = sectoralDevelopmentsChangesStore();

    const { selectedDevelopment, setSelectedDevelopment } =
        selectedDevelopmentStore();

    const { selectedAreaDivision } = useAreaDivisionStore();
    const { original, setOriginal } = useDragersStore();

    function saveInput(event, projectId) {
        //if header is set to original - set to aangepast
        original && setOriginal(false);

        let inputvalue = parseFloat(event.target.value);

        if (inputvalue < parseFloat(event.target.min)) {
            inputvalue = event.target.min;
        }
        if (inputvalue > parseFloat(event.target.max)) {
            inputvalue = event.target.max;
        }

        const devKey = event.target.getAttribute('data-develop-input');

        // Zoek naar bestaande project binnen changedSectoralDevelopments
        const existingProjectIndex = changedSectoralDevelopments.findIndex(
            (sd) =>
                sd.municipalityID === gid &&
                sd.devGroupKey === selectedDevelopment.key &&
                sd.projectId === projectId
        );

        let newChangedSectoralDevelopments = [...changedSectoralDevelopments];

        if (existingProjectIndex > -1) {
            // Als project al bestaat, update de specifieke devKey
            const existingProject =
                changedSectoralDevelopments[existingProjectIndex];

            existingProject.isDefault = false;

            const changeIndex = existingProject.changes.findIndex(
                (change) => change.devKey === devKey
            );

            if (changeIndex > -1) {
                // Update bestaande wijziging
                existingProject.changes[changeIndex].value = inputvalue;
            } else {
                // Voeg nieuwe wijziging toe
                existingProject.isDefault = false;
                existingProject.changes.push({
                    devKey: devKey,
                    value: inputvalue,
                    unit: event.target.getAttribute('data-develop-unit') || '',
                });
            }

            // Werk de changedSectoralDevelopments bij met de bijgewerkte ontwikkeling
            newChangedSectoralDevelopments = [
                ...changedSectoralDevelopments.slice(0, existingProjectIndex),
                existingProject,
                ...changedSectoralDevelopments.slice(existingProjectIndex + 1),
            ];
        } else {
            //Zoek naar default ontwikkeling
            const developmentDefault = developments.filter(
                (dev) =>
                    dev.type === 'sectoral' &&
                    dev.key === selectedDevelopment.key
            )[0];

            // En voeg een project voor deze ontwikkeling toe
            const devInputOptions = developmentDefault.inputs;

            newChangedSectoralDevelopments = [
                ...changedSectoralDevelopments,
                {
                    devGroupKey: selectedDevelopment.key,
                    projectId: projectId,
                    municipalityID: gid,
                    isDefault: false,
                    changes: devInputOptions.map((option) => {
                        return {
                            devKey: option.key,
                            value:
                                option.key === devKey
                                    ? inputvalue
                                    : option.default,
                            unit: option.unit,
                        };
                    }),
                },
            ];
        }
        setChangedSectoralDevelopments(newChangedSectoralDevelopments);
    }

    function toggleOrSetActiveID(id) {
        if (selectedDevelopment && selectedDevelopment.key === id) {
            setSelectedDevelopment(null);
            setNewProjectOpen(false);
        } else {
            const development = developments.find(
                (development) => development.key === id
            );
            setSelectedDevelopment({
                key: id,
                type: 'sd',
                name: development.name,
                min: development.inputs[0].min,
                max: development.inputs[0].max,
                unit: development.inputs[0].unit,
            });
        }
    }

    function toggleProject(projectKey) {
        setExpandedProjects((prev) => {
            if (prev.includes(projectKey)) {
                return prev.filter((p) => p !== projectKey);
            } else {
                return [...prev, projectKey];
            }
        });
    }

    function checkProjects(development) {
        if (original && selectedAreaDivision === 'GM') {
            return sectoralDevelopmentDefaultProjects.filter(
                (sd) =>
                    sd.municipalityID === gid &&
                    sd.devGroupKey === development.key
            );
        }
        //check if there are any projects for this development
        let addedProjects;
        //if selected area is in GM this will be in changedSectoralDevelopments
        if (selectedAreaDivision === 'GM') {
            addedProjects = changedSectoralDevelopments.filter(
                (sd) =>
                    sd.municipalityID === gid &&
                    sd.devGroupKey === development.key
            );
            //else if is a different state where you can only view the projects and not interact with them
        } else {
            addedProjects = aggregatedProjects.filter(
                (sd) =>
                    sd.municipalityID === gid &&
                    sd.devGroupKey === development.key
            );
        }
        if (addedProjects.length > 0) {
            return addedProjects;
        } else {
            return [];
        }
    }

    function deleteProject(projectId) {
        setChangedSectoralDevelopments(
            changedSectoralDevelopments.filter(
                (sd) => sd.projectId !== projectId
            )
        );
    }

    function saveNewProject(project) {
        //if header is set to original - set to aangepast
        original && setOriginal(false);

        setChangedSectoralDevelopments([
            ...changedSectoralDevelopments,
            project,
        ]);
    }

    return (
        <RadioGroup className="flex flex-col flex-1 overflow-y-auto">
            <div className={`flex items-center flex-col justify-between gap-2`}>
                {developments &&
                    developments.length > 0 &&
                    developments.map((development: any, index: any) => {
                        const developmentKey = development.key;

                        const projects = checkProjects(development);

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
                                            className={` ${developmentKey == selectedDevelopment?.key && 'text-white '} ${s.ButtonWithSwitch__label} truncate`}>
                                            {development.name ||
                                                development.label}
                                        </small>
                                        {/* to do: data is missing, so this can not be shown right now */}
                                        <div className="ml-auto">
                                            <small
                                                className={` ${developmentKey == selectedDevelopment?.key && 'text-white '}`}>
                                                {Math.round(
                                                    projects
                                                        .map(
                                                            (project) =>
                                                                project.changes
                                                        )
                                                        .flat()
                                                        .reduce(
                                                            (partialSum, a) =>
                                                                parseFloat(
                                                                    partialSum
                                                                ) +
                                                                parseFloat(
                                                                    a.value
                                                                ),
                                                            0
                                                        )
                                                )}{' '}
                                                {development.inputs[0].unit ||
                                                    'units'}
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
                                    {/* to do: data is missing, so this can not be shown right now */}
                                    <div className="flex flex-row justify-between align-center">
                                        <small
                                            className={` ${developmentKey == selectedDevelopment?.key && 'text-white '}`}>
                                            {Math.round(
                                                projects
                                                    .map(
                                                        (project) =>
                                                            project.changes
                                                    )
                                                    .flat()
                                                    .reduce(
                                                        (partialSum, a) =>
                                                            parseFloat(
                                                                partialSum
                                                            ) +
                                                            parseFloat(a.value),
                                                        0
                                                    )
                                            )}{' '}
                                            {development.inputs[0].unit ||
                                                'units'}
                                        </small>
                                        <small
                                            className={` ${developmentKey == selectedDevelopment?.key && 'text-white '}`}>
                                            {projects.length} project(en)
                                        </small>
                                    </div>
                                    {/* if sectoral dev is selected it will show projects */}
                                    {/*gid && (
                                        <SummaryTable
                                            gid={gid}
                                            developmentkey={development.key}
                                        />
                                    )*/}
                                    {allExpandedRows &&
                                        selectedDevelopment?.key ===
                                            developmentKey && (
                                            <div
                                                className={`${s.ButtonWithSwitch__details}`}>
                                                <div className="flex flex-col gap-4 w-full">
                                                    {projects &&
                                                        projects.map(
                                                            (
                                                                developmentProject,
                                                                index
                                                            ) => (
                                                                <div
                                                                    key={index}
                                                                    className="flex flex-col gap-2 w-full">
                                                                    <div
                                                                        className="flex items-center justify-between cursor-pointer"
                                                                        onClick={(
                                                                            e
                                                                        ) => {
                                                                            e.stopPropagation();

                                                                            toggleProject(
                                                                                developmentProject.projectId
                                                                            );
                                                                        }}>
                                                                        <div className="flex flex-row items-center">
                                                                            <span
                                                                                className={`${s.ButtonWithSwitch__details__right}`}>
                                                                                {expandedProjects.includes(
                                                                                    developmentProject.projectId
                                                                                ) ? (
                                                                                    <ChevronDownIcon className="h-4 w-4" />
                                                                                ) : (
                                                                                    <ChevronRightIcon className="h-4 w-4" />
                                                                                )}
                                                                            </span>

                                                                            <span className="ml-4">
                                                                                {
                                                                                    developmentProject.projectName
                                                                                }
                                                                            </span>
                                                                        </div>

                                                                        <span
                                                                            onClick={(
                                                                                e
                                                                            ) => {
                                                                                deleteProject(
                                                                                    developmentProject.projectId
                                                                                );
                                                                                e.stopPropagation();
                                                                            }}
                                                                            className={`${s.ButtonWithSwitch__details__right}`}>
                                                                            <TrashIcon className="h-4 w-4" />
                                                                        </span>
                                                                    </div>
                                                                    {/* if project dev is selected it will show input values */}
                                                                    {expandedProjects.includes(
                                                                        developmentProject.projectId
                                                                    ) &&
                                                                        developmentProject.changes.map(
                                                                            (
                                                                                developmentInput,
                                                                                index
                                                                            ) => (
                                                                                <Development
                                                                                    key={
                                                                                        index
                                                                                    }
                                                                                    gid={
                                                                                        gid
                                                                                    }
                                                                                    saveInput={
                                                                                        saveInput
                                                                                    }
                                                                                    developmentInput={
                                                                                        developmentInput
                                                                                    }
                                                                                    developmentKey={
                                                                                        developmentKey
                                                                                    }
                                                                                    developmentType="sectoral"
                                                                                    changedDevelopments={
                                                                                        selectedAreaDivision ===
                                                                                        'GM'
                                                                                            ? changedSectoralDevelopments
                                                                                            : aggregatedProjects
                                                                                    }
                                                                                    selectedDevelopment={
                                                                                        selectedDevelopment
                                                                                    }
                                                                                    selectedAreaDivision={
                                                                                        selectedAreaDivision
                                                                                    }
                                                                                    projectId={
                                                                                        developmentProject.projectId
                                                                                    }></Development>
                                                                            )
                                                                        )}
                                                                </div>
                                                            )
                                                        )}
                                                    {selectedAreaDivision ===
                                                        'GM' && (
                                                        <div className="flex flex-col justify-center">
                                                            {newProjectOpen ? (
                                                                <SectoralNewProject
                                                                    development={
                                                                        development
                                                                    }
                                                                    setOpen={
                                                                        setNewProjectOpen
                                                                    }
                                                                    saveProject={
                                                                        saveNewProject
                                                                    }
                                                                    selectedAreaDivision={
                                                                        selectedAreaDivision
                                                                    }
                                                                    gid={gid}
                                                                />
                                                            ) : (
                                                                <Button
                                                                    variant="outline"
                                                                    className="border-primary"
                                                                    size="sm"
                                                                    onClick={() =>
                                                                        setNewProjectOpen(
                                                                            true
                                                                        )
                                                                    }>
                                                                    Voeg project
                                                                    toe
                                                                </Button>
                                                            )}
                                                        </div>
                                                    )}
                                                </div>
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

{
    /*  {changedSectoralDevelopments.find(
                                                (cd: any) =>
                                                    cd.gid === gid &&
                                                    cd.cd === development.key
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
                                            )} */
}
