import {
    draggable,
    dropTargetForElements,
} from '@atlaskit/pragmatic-drag-and-drop/element/adapter';
import { useEffect, useRef, useState } from 'react';

import styles from './WorkboardPage.module.css';
import {
    ACM_PRIO_OPTIONS,
    ProjectCardProps,
    STATUS_OPTIONS,
} from './Workboardpage';

const ProjectCard = ({
    project,
    canDrag,
    canEdit,
    laneIndex,
    onEdit,
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
            <strong
                className={styles.projectstatus}
                title={
                    ACM_PRIO_OPTIONS.find(
                        (option) => option.value === project.acm_prio
                    )?.label ?? 'Unknown'
                }>
                {project.acm_prio}
            </strong>
            <div className={styles.projectinfo}>
                <strong>{project.title}</strong>
                <p>{project.size_mw} MW</p>
                <div className={styles.badgelist}>
                    <small className={styles.badge}>{project.type}</small>
                    <small className={styles.badge}>
                        {project.organization}
                    </small>
                    <small
                        className={styles.badge}
                        title={
                            STATUS_OPTIONS.find(
                                (option) => option.value === project.status
                            )?.label ?? 'Unknown'
                        }>
                        {project.status < 4 ? 'zacht' : 'hard'}
                    </small>
                </div>
            </div>
            {canEdit && (
                <button
                    className={styles.editbutton}
                    onClick={() => onEdit(project)}
                    type="button">
                    <small className={styles.badge}>edit</small>
                </button>
            )}
        </article>
    );
};

export default ProjectCard;
