import { useState } from 'react';

import CreateItemModal from './CreateItemModal';
import EditItemModal from './EditItemModal';
import ProjectCard from './ProjectCard';
import SwimmingLaneColumn from './SwimmingLaneColumn';
import styles from './WorkboardPage.module.css';
import { PHASE_CHOICES, Project, WorkboardPageProps } from './Workboardpage';
import { useWorkboardProjects } from './useWorkboardProjects';
import { postRequest } from '@/api/requests';

const WorkboardPage = ({
    id,
    title = 'Workboard',
    phase,
    username,
    organization,
    isAdmin,
    swimmingLanes = [],
}: WorkboardPageProps) => {
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
    const [editingProject, setEditingProject] = useState<Project | null>(null);

    const {
        projects,
        isCreating,
        createError,
        isUpdating,
        updateError,
        isDeleting,
        modifications,
        isLoadingModifications,
        handleProjectDrop,
        handleCreateItem: createItem,
        handleUpdateItem: updateItem,
        handleDeleteItem,
        clearCreateError,
        clearUpdateError,
    } = useWorkboardProjects({
        pageId: id,
        editingProject,
        onEditComplete: () => setEditingProject(null),
    });

    const canEditProject = (project: Project) =>
        Boolean(isAdmin) ||
        (phase?.toLowerCase() === 'inzicht & invoeren' &&
            Boolean(organization) &&
            project.organization === organization);
    const organizations = Array.from(
        new Set(projects.map((project) => project.organization).filter(Boolean))
    );

    const handleCreateItem = async (
        itemTitle: string,
        description: string,
        type: Project['type'],
        sizeMw: number,
        status: number,
        acmPrio: number
    ) => {
        const created = await createItem({
            title: itemTitle,
            description,
            type,
            size_mw: sizeMw,
            acm_prio: acmPrio,
            status,
        });
        if (created) {
            setIsCreateModalOpen(false);
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
        return updateItem({
            title: itemTitle,
            description,
            type,
            size_mw: sizeMw,
            acm_prio: acmPrio,
            status,
        });
    };

     const NEXT_PUBLIC_API_URL: string =
        process.env.NEXT_PUBLIC_WAGTAIL_API_URL || '';

    const handleLogout = async () => {
        try {
            await postRequest(`${NEXT_PUBLIC_API_URL}/v1/logout/`, {});
            // Redirect to home page after logout
            window.location.href = '/';
        } catch (error) {
            console.error('Logout failed:', error);
            // Even if the API call fails, redirect to home
            window.location.href = '/';
        }
    };

    return (
        <>
            <main className={styles.page}>
                {username &&
                    <header className={styles.logoutmenu}>
                        <small>Ingelogd als {username} &nbsp; ({organization})</small> <button onClick={handleLogout}><small className={styles.badge}>Log uit</small></button>
                    </header>
                }
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
                                    clearCreateError();
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
                                            clearUpdateError();
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
                                clearUpdateError();
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
        </>
    );
};

export default WorkboardPage;
