import { dropTargetForElements } from '@atlaskit/pragmatic-drag-and-drop/element/adapter';
import { useEffect, useRef, useState } from 'react';

import ProjectCard from './ProjectCard';
import { SwimmingLaneColumnProps } from './Workboardpage';
import styles from './WorkboardPage.module.css';

const SwimmingLaneColumn = ({
    index,
    lane,
    projects,
    userOrganization,
    isAdmin,
    phase,
    canEdit,
    onEdit,
    onProjectDrop,
}: SwimmingLaneColumnProps) => {
    const columnRef = useRef<HTMLElement>(null);
    const [isDraggedOver, setIsDraggedOver] = useState(false);
    const totalSize = projects.reduce(
        (sum, project) => sum + project.size_mw,
        0
    );

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
            <div className={styles.columnSummary}>
                <h2>{lane.label}</h2>
                <div
                    className={styles.columnProgress}
                    data-max={lane.maximumEnergy + 'MW'}>
                    <span
                        style={{
                            width: `${Math.min((totalSize / lane.maximumEnergy) * 100, 100)}%`,
                        }}
                        className={styles.columnProgressBar}
                        data-max={lane.maximumEnergy}
                        data-value={totalSize}
                        data-label={totalSize + 'MW'}></span>
                </div>
            </div>

            <div className={styles.projects}>
                {projects.map((project) => (
                    <ProjectCard
                        key={project.id}
                        canDrag={
                            Boolean(isAdmin) ||
                            (phase?.toLowerCase() !== 'samenwerksessie' &&
                                Boolean(userOrganization) &&
                                project.organization === userOrganization)
                        }
                        canEdit={canEdit(project)}
                        laneIndex={index}
                        onEdit={onEdit}
                        onProjectDrop={onProjectDrop}
                        project={project}
                    />
                ))}
            </div>
        </article>
    );
};

export default SwimmingLaneColumn;
