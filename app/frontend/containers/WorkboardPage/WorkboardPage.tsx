import {
    draggable,
    dropTargetForElements,
} from '@atlaskit/pragmatic-drag-and-drop/element/adapter';
import { FormEvent, useCallback, useEffect, useRef, useState } from 'react';

import styles from './WorkboardPage.module.css';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

const getCsrfToken = () =>
    document.cookie
        .split('; ')
        .find((cookie) => cookie.startsWith('csrftoken='))
        ?.split('=')[1];

export type SwimmingLane = {
    label: string;
    minimumEnergy: number;
    maximumEnergy: number;
    minimumRisk: number;
    maximumRisk: number;
};

type Project = {
    id: number;
    title: string;
    description: string;
    organization: string;
    user: number;
    lane: number;
};

interface WorkboardPageProps {
    id: number;
    title?: string;
    phase?: string;
    organization?: string | null;
    swimmingLanes?: SwimmingLane[];
}

interface SwimmingLaneColumnProps {
    index: number;
    lane: SwimmingLane;
    projects: Project[];
    userOrganization?: string | null;
    onProjectDrop: (
        projectId: number,
        laneIndex: number,
        targetProjectId?: number,
        insertBefore?: boolean
    ) => void;
}

interface ProjectCardProps {
    project: Project;
    canDrag: boolean;
    laneIndex: number;
    onProjectDrop: SwimmingLaneColumnProps['onProjectDrop'];
}

interface CreateItemModalProps {
    isOpen: boolean;
    isSubmitting: boolean;
    error?: string;
    onClose: () => void;
    onSubmit: (title: string, description: string) => void;
}

const CreateItemModal = ({
    isOpen,
    isSubmitting,
    error,
    onClose,
    onSubmit,
}: CreateItemModalProps) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');

    useEffect(() => {
        if (!isOpen) {
            setTitle('');
            setDescription('');
        }
    }, [isOpen]);

    if (!isOpen) {
        return null;
    }

    const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        onSubmit(title, description);
    };

    return (
        <div className={styles.modalBackdrop} role="presentation">
            <section
                aria-labelledby="create-item-title"
                aria-modal="true"
                className={styles.modal}
                role="dialog">
                <div className={styles.modalHeader}>
                    <div>
                        <p className={styles.eyebrow}>Lane 0</p>
                        <h2 id="create-item-title">Create new item</h2>
                    </div>
                    <button
                        aria-label="Close modal"
                        className={styles.closeButton}
                        onClick={onClose}
                        type="button">
                        x
                    </button>
                </div>
                <form className={styles.form} onSubmit={handleSubmit}>
                    <label htmlFor="item-title">Title</label>
                    <input
                        autoFocus
                        id="item-title"
                        onChange={(event) => setTitle(event.target.value)}
                        required
                        value={title}
                    />
                    <label htmlFor="item-description">Description</label>
                    <textarea
                        id="item-description"
                        onChange={(event) => setDescription(event.target.value)}
                        rows={5}
                        value={description}
                    />
                    {error && <p className={styles.formError}>{error}</p>}
                    <div className={styles.modalActions}>
                        <button
                            className={styles.secondaryButton}
                            onClick={onClose}
                            type="button">
                            Cancel
                        </button>
                        <button
                            className={styles.primaryButton}
                            disabled={isSubmitting}
                            type="submit">
                            {isSubmitting ? 'Creating...' : 'Create item'}
                        </button>
                    </div>
                </form>
            </section>
        </div>
    );
};

const ProjectCard = ({
    project,
    canDrag,
    laneIndex,
    onProjectDrop,
}: ProjectCardProps) => {
    const cardRef = useRef<HTMLElement>(null);
    const [isDragging, setIsDragging] = useState(false);
    const [isDropTarget, setIsDropTarget] = useState(false);

    useEffect(() => {
        const card = cardRef.current;
        if (!card) {
            return;
        }

        const cleanupDraggable = canDrag
            ? draggable({
                  element: card,
                  getInitialData: () => ({
                      type: 'project',
                      projectId: project.id,
                      organization: project.organization,
                  }),
                  onDragStart: () => setIsDragging(true),
                  onDrop: () => setIsDragging(false),
              })
            : undefined;

        const cleanupDropTarget = dropTargetForElements({
            element: card,
            getData: () => ({
                type: 'project-card',
                projectId: project.id,
            }),
            onDragEnter: () => setIsDropTarget(true),
            onDragLeave: () => setIsDropTarget(false),
            onDrop: ({ source, location }) => {
                const sourceProjectId = source.data.projectId;
                if (
                    source.data.type === 'project' &&
                    typeof sourceProjectId === 'number' &&
                    sourceProjectId !== project.id
                ) {
                    const bounds = card.getBoundingClientRect();
                    const insertBefore =
                        location.current.input.clientY <
                        bounds.top + bounds.height / 2;
                    onProjectDrop(
                        sourceProjectId,
                        laneIndex,
                        project.id,
                        insertBefore
                    );
                }
                setIsDropTarget(false);
            },
        });

        return () => {
            cleanupDraggable?.();
            cleanupDropTarget();
        };
    }, [canDrag, laneIndex, onProjectDrop, project.id, project.organization]);

    return (
        <article
            className={`${styles.project} ${
                isDragging ? styles.projectDragging : ''
            } ${isDropTarget ? styles.projectDropTarget : ''}`}
            ref={cardRef}>
            <span className={styles.projectId}>#{project.id}</span>
            <h3>{project.title}</h3>
            <p>
                {project.organization} | {project.user}
            </p>
            {project.description && <p>{project.description}</p>}
        </article>
    );
};

const SwimmingLaneColumn = ({
    index,
    lane,
    projects,
    userOrganization,
    onProjectDrop,
}: SwimmingLaneColumnProps) => {
    const columnRef = useRef<HTMLElement>(null);
    const [isDraggedOver, setIsDraggedOver] = useState(false);

    useEffect(() => {
        const column = columnRef.current;
        if (!column) {
            return;
        }

        return dropTargetForElements({
            element: column,
            getData: () => ({
                type: 'swimming-lane',
                label: lane.label,
            }),
            onDrop: ({ source, location }) => {
                if (
                    location.current.dropTargets[0]?.data.type !==
                    'swimming-lane'
                ) {
                    setIsDraggedOver(false);
                    return;
                }
                const projectId = source.data.projectId;
                if (
                    source.data.type === 'project' &&
                    typeof projectId === 'number'
                ) {
                    onProjectDrop(projectId, index);
                }
                setIsDraggedOver(false);
            },
            onDragEnter: () => setIsDraggedOver(true),
            onDragLeave: () => setIsDraggedOver(false),
        });
    }, [index, lane.label, onProjectDrop]);

    return (
        <article
            className={`${styles.column} ${
                isDraggedOver ? styles.columnDraggedOver : ''
            }`}
            data-index={index}
            ref={columnRef}>
            <h2>{lane.label}</h2>
            <div className={styles.projects}>
                {projects.map((project) => (
                    <ProjectCard
                        key={project.id}
                        canDrag={
                            Boolean(userOrganization) &&
                            project.organization === userOrganization
                        }
                        laneIndex={index}
                        onProjectDrop={onProjectDrop}
                        project={project}
                    />
                ))}
            </div>
            <dl className={styles.metrics}>
                <div>
                    <dt>Energy</dt>
                    <dd>
                        {lane.minimumEnergy} - {lane.maximumEnergy}
                    </dd>
                </div>
                <div>
                    <dt>Risk</dt>
                    <dd>
                        {lane.minimumRisk} - {lane.maximumRisk}
                    </dd>
                </div>
            </dl>
        </article>
    );
};

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
                    `${API_URL}/workboarditems/item/${projectId}/lane/`,
                    {
                        method: 'PATCH',
                        credentials: 'include',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCsrfToken() || '',
                        },
                        body: JSON.stringify({ lane: laneIndex }),
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

    const handleCreateItem = async (itemTitle: string, description: string) => {
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
