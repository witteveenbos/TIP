import { FormEvent, useEffect, useState } from 'react';

import styles from './WorkboardPage.module.css';
import {
    ACM_PRIO_OPTIONS,
    CreateItemModalProps,
    ProjectType,
    STATUS_OPTIONS,
    TYPE_OPTIONS,
} from './Workboardpage';

const CreateItemModal = ({
    isOpen,
    isSubmitting,
    error,
    onClose,
    onSubmit,
}: CreateItemModalProps) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [type, setType] = useState<ProjectType>(TYPE_OPTIONS[0]);
    const [sizeMw, setSizeMw] = useState('0');
    const [status, setStatus] = useState(1);
    const [acmPrio, setacmPrio] = useState(0);

    useEffect(() => {
        if (!isOpen) {
            setTitle('');
            setDescription('');
            setType(TYPE_OPTIONS[0]);
            setSizeMw('0');
            setStatus(1);
            setacmPrio(0);
        }
    }, [isOpen]);

    if (!isOpen) {
        return null;
    }

    const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        onSubmit(title, description, type, Number(sizeMw), status, acmPrio);
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
                    <label htmlFor="item-type">Type</label>
                    <select
                        id="item-type"
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
                    <label htmlFor="item-size-mw">Size (MW)</label>
                    <input
                        id="item-size-mw"
                        min="0"
                        onChange={(event) => setSizeMw(event.target.value)}
                        required
                        type="number"
                        value={sizeMw}
                    />
                    <label htmlFor="item-status">Status</label>
                    <select
                        id="item-status"
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
                    <label htmlFor="item-acmPrio">ACM priority</label>
                    <select
                        id="item-acmPrio"
                        onChange={(event) =>
                            setacmPrio(Number(event.target.value))
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

export default CreateItemModal;
