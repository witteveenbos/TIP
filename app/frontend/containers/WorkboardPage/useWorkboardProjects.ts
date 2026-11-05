import { useCallback, useEffect, useState } from 'react';

import type { Project, ProjectModification } from './Workboardpage';
import {
    createProject,
    deleteProject,
    getModifications,
    getProjects,
    moveProject,
    updateProject,
} from './workboardApi';

type ProjectInput = Pick<
    Project,
    'title' | 'description' | 'type' | 'size_mw' | 'acm_prio' | 'status'
>;

interface UseWorkboardProjectsProps {
    pageId: number;
    editingProject: Project | null;
    onEditComplete: () => void;
}

export const useWorkboardProjects = ({
    pageId,
    editingProject,
    onEditComplete,
}: UseWorkboardProjectsProps) => {
    const [projects, setProjects] = useState<Project[]>([]);
    const [isCreating, setIsCreating] = useState(false);
    const [createError, setCreateError] = useState<string>();
    const [isUpdating, setIsUpdating] = useState(false);
    const [updateError, setUpdateError] = useState<string>();
    const [isDeleting, setIsDeleting] = useState(false);
    const [modifications, setModifications] = useState<ProjectModification[]>(
        []
    );
    const [isLoadingModifications, setIsLoadingModifications] = useState(false);

    useEffect(() => {
        let isMounted = true;

        getProjects(pageId)
            .then((loadedProjects) => {
                if (isMounted) {
                    setProjects(loadedProjects);
                }
            })
            .catch(() => {
                if (isMounted) {
                    setProjects([]);
                }
            });

        return () => {
            isMounted = false;
        };
    }, [pageId]);

    useEffect(() => {
        if (!editingProject) {
            setModifications([]);
            return;
        }

        let isMounted = true;
        setIsLoadingModifications(true);

        getModifications(editingProject.id)
            .then((loadedModifications) => {
                if (isMounted) {
                    setModifications(loadedModifications);
                }
            })
            .catch(() => {
                if (isMounted) {
                    setModifications([]);
                }
            })
            .finally(() => {
                if (isMounted) {
                    setIsLoadingModifications(false);
                }
            });

        return () => {
            isMounted = false;
        };
    }, [editingProject]);

    const handleProjectDrop = useCallback(
        async (
            projectId: number,
            laneIndex: number,
            targetProjectId?: number,
            insertBefore = false
        ) => {
            try {
                await moveProject(
                    projectId,
                    laneIndex,
                    targetProjectId,
                    insertBefore
                );

                setProjects((currentProjects) => {
                    const project = currentProjects.find(
                        (item) => item.id === projectId
                    );
                    if (!project) {
                        return currentProjects;
                    }

                    const withoutProject = currentProjects.filter(
                        (item) => item.id !== projectId
                    );
                    const movedProject = { ...project, lane: laneIndex };

                    if (targetProjectId !== undefined) {
                        const targetIndex = withoutProject.findIndex(
                            (item) => item.id === targetProjectId
                        );
                        if (targetIndex !== -1) {
                            withoutProject.splice(
                                insertBefore ? targetIndex : targetIndex + 1,
                                0,
                                movedProject
                            );
                            return withoutProject;
                        }
                    }

                    const lastLaneIndex = withoutProject.reduce(
                        (lastIndex, item, index) =>
                            item.lane === laneIndex ? index : lastIndex,
                        -1
                    );
                    withoutProject.splice(lastLaneIndex + 1, 0, movedProject);
                    return withoutProject;
                });
            } catch {
                return;
            }
        },
        []
    );

    const handleCreateItem = async (project: ProjectInput) => {
        setIsCreating(true);
        setCreateError(undefined);

        try {
            const createdProject = await createProject(pageId, project);
            setProjects((currentProjects) => [
                createdProject,
                ...currentProjects,
            ]);
            return true;
        } catch {
            setCreateError('Fout bij aanmaken van item, probeer het opnieuw.');
            return false;
        } finally {
            setIsCreating(false);
        }
    };

    const handleUpdateItem = async (project: ProjectInput) => {
        if (!editingProject) {
            return false;
        }

        setIsUpdating(true);
        setUpdateError(undefined);

        try {
            const updatedProject = await updateProject(
                editingProject.id,
                project
            );
            setProjects((currentProjects) =>
                currentProjects.map((currentProject) =>
                    currentProject.id === updatedProject.id
                        ? updatedProject
                        : currentProject
                )
            );
            onEditComplete();
            return true;
        } catch {
            setUpdateError('Fout bij updaten van item, probeer het opnieuw.');
            return false;
        } finally {
            setIsUpdating(false);
        }
    };

    const handleDeleteItem = async () => {
        if (!editingProject) {
            return false;
        }

        setIsDeleting(true);
        setUpdateError(undefined);

        try {
            await deleteProject(editingProject.id);
            setProjects((currentProjects) =>
                currentProjects.filter(
                    (project) => project.id !== editingProject.id
                )
            );
            onEditComplete();
            return true;
        } catch {
            setUpdateError(
                'Fout bij verwijderen van item. Probeer het opnieuw.'
            );
            return false;
        } finally {
            setIsDeleting(false);
        }
    };

    return {
        projects,
        isCreating,
        createError,
        isUpdating,
        updateError,
        isDeleting,
        modifications,
        isLoadingModifications,
        handleProjectDrop,
        handleCreateItem,
        handleUpdateItem,
        handleDeleteItem,
        clearCreateError: () => setCreateError(undefined),
        clearUpdateError: () => setUpdateError(undefined),
    };
};
