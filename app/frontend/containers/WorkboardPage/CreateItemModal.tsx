import ItemForm, { ItemFormValues } from './ItemForm';
import { CreateItemModalProps } from './Workboardpage';
import styles from './WorkboardPage.module.css';

const CreateItemModal = ({
    isOpen,
    isSubmitting,
    error,
    onClose,
    onSubmit,
}: CreateItemModalProps) => {
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

    return (
        <div className={styles.modalBackdrop} role="presentation">
            <section
                aria-labelledby="create-item-title"
                aria-modal="true"
                className={styles.modal}
                role="dialog">
                <div className={styles.modalHeader}>
                    <div>
                        <h2 id="create-item-title">Maak nieuw item</h2>
                    </div>
                    <button
                        aria-label="sluit venster"
                        className={styles.closeButton}
                        onClick={onClose}
                        type="button">
                        x
                    </button>
                </div>
                <ItemForm
                    error={error}
                    idPrefix="item"
                    initialValues={{
                        title: '',
                        description: '',
                        type: 'Woningbouw',
                        sizeMw: 0,
                        status: 1,
                        acmPrio: 0,
                    }}
                    isSubmitting={isSubmitting}
                    onCancel={onClose}
                    onSubmit={handleSubmit}
                    submitLabel="Verstuur"
                    submittingLabel="Aanmaken..."
                />
            </section>
        </div>
    );
};

export default CreateItemModal;
