import { useCallback, useEffect, useState } from 'react';

import CreateItemModal from './CreateItemModal';
import ProjectCard from './ProjectCard';
import SwimmingLaneColumn from './SwimmingLaneColumn';
import styles from './WorkboardPage.module.css';
import { Project, WorkboardPageProps } from './Workboardpage';

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
    swimmingLanes = [],
}: WorkboardPageProps) => {
    const [projects, setProjects] = useState<Project[]>([]);
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
    const [isCreating, setIsCreating] = useState(false);
    const [createError, setCreateError] = useState<string>();

    useEffect(() => {
        let isMounted = true;

        fetch(`${API_URL}/workboarditems/${id}/`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Unable to load projects');
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
                throw new Error('Unable to create item');
            }

            const createdProject = (await response.json()) as Project;
            setProjects((currentProjects) => [
                createdProject,
                ...currentProjects,
            ]);
            setIsCreateModalOpen(false);
        } catch {
            setCreateError('Unable to create item. Please try again.');
        } finally {
            setIsCreating(false);
        }
    };

    return (
        <main className={styles.page}>
            <header className={styles.header}>
                <div>
                    <p className={styles.eyebrow}>Workboard</p>
                    <h1>{title}</h1>
                </div>
                {phase && <p className={styles.phase}>{phase}</p>}
            </header>

            <section className={styles.board} aria-label="Swimming lanes">
                <article className={styles.column}>
                    <div className={styles.laneHeader}>
                        <div>
                            <p className={styles.laneNumber}>Lane 0</p>
                            <h2>New items</h2>
                            <p className={styles.laneTotal}>
                                Total size:{' '}
                                {projects
                                    .filter((project) => project.lane === 0)
                                    .reduce(
                                        (sum, project) => sum + project.size_mw,
                                        0
                                    )}{' '}
                                MW
                            </p>
                        </div>
                        <button
                            className={styles.primaryButton}
                            onClick={() => {
                                setCreateError(undefined);
                                setIsCreateModalOpen(true);
                            }}
                            type="button">
                            Create new item
                        </button>
                    </div>
                    <div className={styles.projects}>
                        {projects
                            .filter((project) => project.lane === 0)
                            .map((project) => (
                                <ProjectCard
                                    key={project.id}
                                    canDrag={
                                        Boolean(organization) &&
                                        project.organization === organization
                                    }
                                    laneIndex={0}
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
        </main>
    );
};

export default WorkboardPage;
