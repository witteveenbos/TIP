import { useEffect, useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import Development from './Development';
import s from './EnergyBalance.module.css';

export default function SectoralNewProject({
    development,
    saveProject,
    setOpen,
    selectedAreaDivision,
    gid,
}) {
    const [newProject, setNewProject] = useState({});
    const projectId = `project-${development.key}-${uuidv4()}`;

    useEffect(() => {
        setNewProject({
            projectName: '',
            devGroupKey: development.key,
            changes: development.inputs.map((input) => ({
                devKey: input.key,
                value: input.default,
                unit: input.unit,
            })),
            projectId: projectId,
            municipalityID: gid,
            isDefault: false,
        });
    }, []);

    function handleCloseProject() {
        setNewProject({});
        setOpen(false);
    }

    function handleSaveProject() {
        saveProject(newProject);
        setNewProject({});
        setOpen(false);
    }

    function handleInputChange(e: React.ChangeEvent<HTMLInputElement>): void {
        e.preventDefault();

        setNewProject({
            ...newProject,
            changes: newProject.changes.map((input) => {
                if (
                    input.devKey === e.target.getAttribute('data-develop-input')
                ) {
                    return { ...input, value: e.target.value };
                }
                return input;
            }),
        });
    }

    function handleNameChange(e: React.ChangeEvent<HTMLInputElement>): void {
        e.preventDefault();
        setNewProject({ ...newProject, [e.target.name]: e.target.value });
    }

    return (
        <div className="flex flex-col gap-2 w-full ">
            <h5 className={s.SectoralNewProject__title}>
                Nieuw project van dit type toevoegen
            </h5>
            <div className="pr-12">
                <Input
                    type="text"
                    placeholder="Project naam"
                    name="projectName"
                    title="Project naam"
                    disabled={selectedAreaDivision !== 'GM'}
                    id="projectName"
                    onChange={(e) => handleNameChange(e)}
                    value={newProject.projectName}
                />
            </div>

            {development.inputs.map((input, index) => (
                <Development
                    key={index}
                    developmentKey={development.key}
                    developmentInput={input}
                    saveInput={handleInputChange}
                    selectedAreaDivision={selectedAreaDivision}
                    developmentType="sectoral"
                />
            ))}
            <div className="flex flex-row justify-between w-full px-12 py-2 ">
                <Button
                    variant="outline"
                    className="border-primary"
                    size="sm"
                    onClick={() => handleCloseProject()}>
                    Annuleren
                </Button>
                <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleSaveProject()}>
                    Opslaan
                </Button>
            </div>
        </div>
    );
}
