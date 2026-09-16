import { useCallback, useEffect, useState } from 'react';

import CreateItemModal from './CreateItemModal';
import EditItemModal from './EditItemModal';
import ProjectCard from './ProjectCard';
import SwimmingLaneColumn from './SwimmingLaneColumn';
import styles from './WorkboardPage.module.css';
import {
    PHASE_CHOICES,
    Project,
    ProjectModification,
    WorkboardPageProps,
} from './Workboardpage';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

const getCsrfToken = () =>
    document.cookie
        .split('; ')
        .find((cookie) => cookie.startsWith('csrftoken='))
        ?.split('=')[1];

const WorkboardPage = ({
    id,
    title = 'Workboard',
    phase,
    organization,
    isAdmin,
    swimmingLanes = [],
}: WorkboardPageProps) => {
    const [projects, setProjects] = useState<Project[]>([]);
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
    const [isCreating, setIsCreating] = useState(false);
    const [createError, setCreateError] = useState<string>();
    const [editingProject, setEditingProject] = useState<Project | null>(null);
    const [isUpdating, setIsUpdating] = useState(false);
    const [updateError, setUpdateError] = useState<string>();
    const [isDeleting, setIsDeleting] = useState(false);
    const [modifications, setModifications] = useState<ProjectModification[]>(
        []
    );
    const [isLoadingModifications, setIsLoadingModifications] = useState(false);

    const canEditProject = (project: Project) =>
        Boolean(isAdmin) ||
        (phase?.toLowerCase() === 'inzicht & invoeren' &&
            Boolean(organization) &&
            project.organization === organization);
    const organizations = Array.from(
        new Set(projects.map((project) => project.organization).filter(Boolean))
    );

    useEffect(() => {
        let isMounted = true;

        fetch(`${API_URL}/workboarditems/${id}/`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Fout bij inladen van projecten');
                }
                return response.json();
            })
            .then((loadedProjects: Project[]) => {
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
    }, [id]);

    useEffect(() => {
        if (!editingProject) {
            setModifications([]);
            return;
        }

        let isMounted = true;
        setIsLoadingModifications(true);
        fetch(
            `${API_URL}/workboarditems/item/${editingProject.id}/modifications/`,
            { credentials: 'include' }
        )
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Fout bij inladen van modificaties');
                }
                return response.json();
            })
            .then((loadedModifications: ProjectModification[]) => {
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
                const response = await fetch(
                    `${API_URL}/workboarditems/item/${projectId}/position/`,
                    {
                        method: 'PATCH',
                        credentials: 'include',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCsrfToken() || '',
                        },
                        body: JSON.stringify({
                            lane: laneIndex,
                            target_item_id: targetProjectId ?? null,
                            insert_before: insertBefore,
                        }),
                    }
                );
                if (!response.ok) {
                    return;
                }

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

    const handleCreateItem = async (
        itemTitle: string,
        description: string,
        type: Project['type'],
        sizeMw: number,
        status: number,
        acmPrio: number
    ) => {
        setIsCreating(true);
        setCreateError(undefined);

        try {
            const response = await fetch(`${API_URL}/workboarditems/${id}/`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken() || '',
                },
                body: JSON.stringify({
                    title: itemTitle,
                    description,
                    type,
                    size_mw: sizeMw,
                    acm_prio: acmPrio,
                    status,
                }),
            });

            if (!response.ok) {
                throw new Error('Fout bij aanmaken van item');
            }

            const createdProject = (await response.json()) as Project;
            setProjects((currentProjects) => [
                createdProject,
                ...currentProjects,
            ]);
            setIsCreateModalOpen(false);
        } catch {
            setCreateError('Fout bij aanmaken van item, probeer het opnieuw.');
        } finally {
            setIsCreating(false);
        }
    };

    const handleUpdateItem = async (
        itemTitle: string,
        description: string,
        type: Project['type'],
        sizeMw: number,
        status: number,
        acmPrio: number
    ) => {
        if (!editingProject) {
            return;
        }

        setIsUpdating(true);
        setUpdateError(undefined);

        try {
            const response = await fetch(
                `${API_URL}/workboarditems/item/${editingProject.id}/`,
                {
                    method: 'PATCH',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken() || '',
                    },
                    body: JSON.stringify({
                        title: itemTitle,
                        description,
                        type,
                        size_mw: sizeMw,
                        acm_prio: acmPrio,
                        status,
                    }),
                }
            );

            if (!response.ok) {
                throw new Error('Fout bij updaten van item');
            }

            const updatedProject = (await response.json()) as Project;
            setProjects((currentProjects) =>
                currentProjects.map((project) =>
                    project.id === updatedProject.id ? updatedProject : project
                )
            );
            setEditingProject(null);
        } catch {
            setUpdateError('Fout bij updaten van item, probeer het opnieuw.');
        } finally {
            setIsUpdating(false);
        }
    };

    const handleDeleteItem = async () => {
        if (!editingProject) {
            return;
        }

        setIsDeleting(true);
        setUpdateError(undefined);

        try {
            const response = await fetch(
                `${API_URL}/workboarditems/item/${editingProject.id}/`,
                {
                    method: 'DELETE',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken': getCsrfToken() || '',
                    },
                }
            );

            if (!response.ok) {
                throw new Error('Fout bij verwijderen van item');
            }

            setProjects((currentProjects) =>
                currentProjects.filter(
                    (project) => project.id !== editingProject.id
                )
            );
            setEditingProject(null);
        } catch {
            setUpdateError(
                'Fout bij verwijderen van item. Probeer het opnieuw.'
            );
        } finally {
            setIsDeleting(false);
        }
    };

    return (
        <main className={styles.page}>
            <header className={styles.header}>
                <ul>
                    {PHASE_CHOICES.map((phaseChoice) => {
                        const isActive =
                            phase === phaseChoice.label ||
                            phase === String(phaseChoice.value);

                        return (
                            <li
                                aria-current={isActive ? 'step' : undefined}
                                className={isActive ? styles.active : undefined}
                                key={phaseChoice.value}>
                                <span>{phaseChoice.value}</span>
                                <span>{phaseChoice.label}</span>
                            </li>
                        );
                    })}
                </ul>
                <ul className={styles.subheader}>
                    <li>
                        <span className={styles.subheader__description}>
                            {
                                PHASE_CHOICES.find(
                                    (phaseChoice) => phaseChoice.label === phase
                                ).description
                            }
                        </span>
                        <span className={styles.badgelist}>
                            {organizations.map((projectOrganization) => (
                                <small
                                    className={styles.badge}
                                    key={projectOrganization}>
                                    {projectOrganization}
                                </small>
                            ))}
                        </span>
                    </li>
                </ul>
            </header>

            <section className={styles.board} aria-label="Swimming lanes">
                <article className={styles.column}>
                    <div className={styles.laneHeader}>
                        <div>
                            <p className={styles.laneNumber}>Voorraad</p>
                        </div>
                        <button
                            className={styles.primaryButton}
                            onClick={() => {
                                setCreateError(undefined);
                                setIsCreateModalOpen(true);
                            }}
                            type="button">
                            Nieuw item
                        </button>
                    </div>
                    <div className={styles.projects}>
                        {projects
                            .filter((project) => project.lane === 0)
                            .map((project) => (
                                <ProjectCard
                                    key={project.id}
                                    canDrag={
                                        Boolean(isAdmin) ||
                                        (phase?.toLowerCase() !==
                                            'samenwerksessie' &&
                                            Boolean(organization) &&
                                            project.organization ===
                                                organization)
                                    }
                                    canEdit={canEditProject(project)}
                                    laneIndex={0}
                                    onEdit={(selectedProject) => {
                                        setUpdateError(undefined);
                                        setEditingProject(selectedProject);
                                    }}
                                    onProjectDrop={handleProjectDrop}
                                    project={project}
                                />
                            ))}
                    </div>
                </article>
                {swimmingLanes.map((lane, index) => (
                    <SwimmingLaneColumn
                        index={index + 1}
                        lane={lane}
                        key={lane.label}
                        projects={projects.filter(
                            (project) => project.lane === index + 1
                        )}
                        userOrganization={organization}
                        isAdmin={isAdmin}
                        phase={phase}
                        canEdit={canEditProject}
                        onEdit={(selectedProject) => {
                            setUpdateError(undefined);
                            setEditingProject(selectedProject);
                        }}
                        onProjectDrop={handleProjectDrop}
                    />
                ))}
            </section>
            <CreateItemModal
                error={createError}
                isOpen={isCreateModalOpen}
                isSubmitting={isCreating}
                onClose={() => setIsCreateModalOpen(false)}
                onSubmit={handleCreateItem}
            />
            {editingProject && (
                <EditItemModal
                    error={updateError}
                    isOpen={true}
                    isSubmitting={isUpdating || isDeleting}
                    onClose={() => setEditingProject(null)}
                    onDelete={handleDeleteItem}
                    onSubmit={handleUpdateItem}
                    project={editingProject}
                    modifications={modifications}
                    isLoadingModifications={isLoadingModifications}
                />
            )}
        </main>
    );
};

export default WorkboardPage;
