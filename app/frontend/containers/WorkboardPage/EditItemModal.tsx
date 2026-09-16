import { FormEvent, useEffect, useState } from 'react';

import styles from './WorkboardPage.module.css';
import {
    ACM_PRIO_OPTIONS,
    EditItemModalProps,
    ProjectModification,
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
    modifications,
    isLoadingModifications,
}: EditItemModalProps) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [type, setType] = useState<ProjectType>(TYPE_OPTIONS[0]);
    const [sizeMw, setSizeMw] = useState('0');
    const [status, setStatus] = useState(1);
    const [acmPrio, setAcmPrio] = useState(0);
    const [activeTab, setActiveTab] = useState<'edit' | 'history'>('edit');

    useEffect(() => {
        if (isOpen) {
            setActiveTab('edit');
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

    const formatModification = (modification: ProjectModification) =>
        `${modification.username ?? 'Onbekende gebruiker'} - ${new Date(
            modification.updated_at
        ).toLocaleString()}`;

    const handleDelete = () => {
        if (
            window.confirm(
                `Weet je zeker dat je "${project.title}" wilt verwijderen?`
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
                        <h2 id="edit-item-title">Aanpassen</h2>
                    </div>
                    <button
                        aria-label="sluit venster"
                        className={styles.closeButton}
                        onClick={onClose}
                        type="button">
                        x
                    </button>
                </div>
                <div className={styles.modalTabs} role="tablist">
                    <button
                        aria-selected={activeTab === 'edit'}
                        className={styles.tabButton}
                        onClick={() => setActiveTab('edit')}
                        role="tab"
                        type="button">
                        Aanpassen
                    </button>
                    <button
                        aria-selected={activeTab === 'history'}
                        className={styles.tabButton}
                        onClick={() => setActiveTab('history')}
                        role="tab"
                        type="button">
                        Historie
                    </button>
                </div>
                {activeTab === 'edit' ? (
                    <form className={styles.form} onSubmit={handleSubmit}>
                        <label htmlFor="edit-item-title-input">Titel</label>
                        <input
                            autoFocus
                            id="edit-item-title-input"
                            onChange={(event) => setTitle(event.target.value)}
                            required
                            value={title}
                        />
                        <label htmlFor="edit-item-description">
                            Omschrijving
                        </label>
                        <textarea
                            id="edit-item-description"
                            onChange={(event) =>
                                setDescription(event.target.value)
                            }
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
                        <label htmlFor="edit-item-size-mw">Grootte (MW)</label>
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
                        <label htmlFor="edit-item-acm-prio">
                            ACM prioriteit
                        </label>
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
                                Verwijder item
                            </button>
                            <button
                                className={styles.secondaryButton}
                                onClick={onClose}
                                type="button">
                                Annuleer
                            </button>
                            <button
                                className={styles.primaryButton}
                                disabled={isSubmitting}
                                type="submit">
                                {isSubmitting ? 'opslaan...' : 'Verstuur'}
                            </button>
                        </div>
                    </form>
                ) : (
                    <div className={styles.history} role="tabpanel">
                        {isLoadingModifications ? (
                            <p>Historie inladen...</p>
                        ) : modifications.length === 0 ? (
                            <p>Nog geen aanpassingen geregistreerd.</p>
                        ) : (
                            <ul>
                                {modifications.map((modification) => (
                                    <li key={modification.id}>
                                        <strong>
                                            {modification.change_type === 'lane'
                                                ? 'Kolom aangepast'
                                                : 'Eigenschap(pen) aangepast'}
                                        </strong>
                                        <span>
                                            {formatModification(modification)}
                                        </span>
                                        {modification.changed_fields.length >
                                            0 && (
                                            <small>
                                                {modification.changed_fields.join(
                                                    ', '
                                                )}
                                            </small>
                                        )}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                )}
            </section>
        </div>
    );
};

export default EditItemModal;
