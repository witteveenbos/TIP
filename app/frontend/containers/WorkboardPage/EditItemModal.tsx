import { useEffect, useState } from 'react';

import ItemForm, { ItemFormValues } from './ItemForm';
import { EditItemModalProps, ProjectModification } from './Workboardpage';
import styles from './WorkboardPage.module.css';

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
    const [activeTab, setActiveTab] = useState<'edit' | 'history'>('edit');

    useEffect(() => {
        if (isOpen) {
            setActiveTab('edit');
        }
    }, [isOpen, project]);

    if (!isOpen) {
        return null;
    }

    const handleSubmit = ({
        title,
        description,
        type,
        sizeMw,
        status,
        acmPrio,
    }: ItemFormValues) =>
        onSubmit(title, description, type, sizeMw, status, acmPrio);

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
                    <ItemForm
                        error={error}
                        idPrefix="edit-item"
                        initialValues={{
                            title: project.title,
                            description: project.description,
                            type: project.type,
                            sizeMw: project.size_mw,
                            status: project.status,
                            acmPrio: project.acm_prio,
                        }}
                        isSubmitting={isSubmitting}
                        onCancel={onClose}
                        onSubmit={handleSubmit}
                        renderAdditionalActions={() => (
                            <button
                                className={styles.deleteButton}
                                disabled={isSubmitting}
                                onClick={handleDelete}
                                type="button">
                                Verwijder item
                            </button>
                        )}
                        submitLabel="Verstuur"
                        submittingLabel="opslaan..."
                    />
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
