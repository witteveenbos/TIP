import { FormEvent, useEffect, useState } from 'react';

import styles from './WorkboardPage.module.css';
import {
    ACM_PRIO_OPTIONS,
    EditItemModalProps,
    ProjectType,
    STATUS_OPTIONS,
    TYPE_OPTIONS,
} from './Workboardpage';

const EditItemModal = ({
    isOpen,
    isSubmitting,
    error,
    project,
    onClose,
    onDelete,
    onSubmit,
}: EditItemModalProps) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [type, setType] = useState<ProjectType>(TYPE_OPTIONS[0]);
    const [sizeMw, setSizeMw] = useState('0');
    const [status, setStatus] = useState(1);
    const [acmPrio, setAcmPrio] = useState(0);

    useEffect(() => {
        if (isOpen) {
            setTitle(project.title);
            setDescription(project.description);
            setType(project.type);
            setSizeMw(String(project.size_mw));
            setStatus(project.status);
            setAcmPrio(project.acm_prio);
        }
    }, [isOpen, project]);

    if (!isOpen) {
        return null;
    }

    const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        onSubmit(title, description, type, Number(sizeMw), status, acmPrio);
    };

    const handleDelete = () => {
        if (
            window.confirm(
                `Are you sure you want to delete "${project.title}"?`
            )
        ) {
            onDelete();
        }
    };

    return (
        <div className={styles.modalBackdrop} role="presentation">
            <section
                aria-labelledby="edit-item-title"
                aria-modal="true"
                className={styles.modal}
                role="dialog">
                <div className={styles.modalHeader}>
                    <div>
                        <p className={styles.eyebrow}>Project item</p>
                        <h2 id="edit-item-title">Edit item</h2>
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
                    <label htmlFor="edit-item-title-input">Title</label>
                    <input
                        autoFocus
                        id="edit-item-title-input"
                        onChange={(event) => setTitle(event.target.value)}
                        required
                        value={title}
                    />
                    <label htmlFor="edit-item-description">Description</label>
                    <textarea
                        id="edit-item-description"
                        onChange={(event) => setDescription(event.target.value)}
                        rows={5}
                        value={description}
                    />
                    <label htmlFor="edit-item-type">Type</label>
                    <select
                        id="edit-item-type"
                        onChange={(event) =>
                            setType(event.target.value as ProjectType)
                        }
                        value={type}>
                        {TYPE_OPTIONS.map((option) => (
                            <option key={option} value={option}>
                                {option}
                            </option>
                        ))}
                    </select>
                    <label htmlFor="edit-item-size-mw">Size (MW)</label>
                    <input
                        id="edit-item-size-mw"
                        min="0"
                        onChange={(event) => setSizeMw(event.target.value)}
                        required
                        type="number"
                        value={sizeMw}
                    />
                    <label htmlFor="edit-item-status">Status</label>
                    <select
                        id="edit-item-status"
                        onChange={(event) =>
                            setStatus(Number(event.target.value))
                        }
                        value={status}>
                        {STATUS_OPTIONS.map((option) => (
                            <option key={option.value} value={option.value}>
                                {option.value}: {option.label}
                            </option>
                        ))}
                    </select>
                    <label htmlFor="edit-item-acm-prio">ACM priority</label>
                    <select
                        id="edit-item-acm-prio"
                        onChange={(event) =>
                            setAcmPrio(Number(event.target.value))
                        }
                        value={acmPrio}>
                        {ACM_PRIO_OPTIONS.map((option) => (
                            <option key={option.value} value={option.value}>
                                {option.value}: {option.label}
                            </option>
                        ))}
                    </select>
                    {error && <p className={styles.formError}>{error}</p>}
                    <div className={styles.modalActions}>
                        <button
                            className={styles.deleteButton}
                            disabled={isSubmitting}
                            onClick={handleDelete}
                            type="button">
                            Delete item
                        </button>
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
                            {isSubmitting ? 'Saving...' : 'Save changes'}
                        </button>
                    </div>
                </form>
            </section>
        </div>
    );
};

export default EditItemModal;
