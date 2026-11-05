import type { ReactNode } from 'react';
import { FormEvent, useEffect, useState } from 'react';

import styles from './WorkboardPage.module.css';
import {
    ACM_PRIO_OPTIONS,
    ProjectType,
    STATUS_OPTIONS,
    TYPE_OPTIONS,
} from './Workboardpage';

export type ItemFormValues = {
    title: string;
    description: string;
    type: ProjectType;
    sizeMw: number;
    status: number;
    acmPrio: number;
};

interface ItemFormProps {
    initialValues: ItemFormValues;
    isSubmitting: boolean;
    error?: string;
    submitLabel: string;
    submittingLabel: string;
    idPrefix: string;
    onCancel: () => void;
    onSubmit: (values: ItemFormValues) => void;
    renderAdditionalActions?: () => ReactNode;
}

const ItemForm = ({
    initialValues,
    isSubmitting,
    error,
    submitLabel,
    submittingLabel,
    idPrefix,
    onCancel,
    onSubmit,
    renderAdditionalActions,
}: ItemFormProps) => {
    const [title, setTitle] = useState(initialValues.title);
    const [description, setDescription] = useState(initialValues.description);
    const [type, setType] = useState<ProjectType>(initialValues.type);
    const [sizeMw, setSizeMw] = useState(String(initialValues.sizeMw));
    const [status, setStatus] = useState(initialValues.status);
    const [acmPrio, setAcmPrio] = useState(initialValues.acmPrio);

    useEffect(() => {
        setTitle(initialValues.title);
        setDescription(initialValues.description);
        setType(initialValues.type);
        setSizeMw(String(initialValues.sizeMw));
        setStatus(initialValues.status);
        setAcmPrio(initialValues.acmPrio);
    }, [initialValues]);

    const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        onSubmit({
            title,
            description,
            type,
            sizeMw: Number(sizeMw),
            status,
            acmPrio,
        });
    };

    return (
        <form className={styles.form} onSubmit={handleSubmit}>
            <label htmlFor={`${idPrefix}-title`}>Titel</label>
            <input
                autoFocus
                id={`${idPrefix}-title`}
                onChange={(event) => setTitle(event.target.value)}
                required
                value={title}
            />
            <label htmlFor={`${idPrefix}-description`}>Omschrijving</label>
            <textarea
                id={`${idPrefix}-description`}
                onChange={(event) => setDescription(event.target.value)}
                rows={5}
                value={description}
            />
            <label htmlFor={`${idPrefix}-type`}>Type</label>
            <select
                id={`${idPrefix}-type`}
                onChange={(event) => setType(event.target.value as ProjectType)}
                value={type}>
                {TYPE_OPTIONS.map((option) => (
                    <option key={option} value={option}>
                        {option}
                    </option>
                ))}
            </select>
            <label htmlFor={`${idPrefix}-size-mw`}>Grootte (MW)</label>
            <input
                id={`${idPrefix}-size-mw`}
                min="0"
                onChange={(event) => setSizeMw(event.target.value)}
                required
                type="number"
                value={sizeMw}
            />
            <label htmlFor={`${idPrefix}-status`}>Status</label>
            <select
                id={`${idPrefix}-status`}
                onChange={(event) => setStatus(Number(event.target.value))}
                value={status}>
                {STATUS_OPTIONS.map((option) => (
                    <option key={option.value} value={option.value}>
                        {option.value}: {option.label}
                    </option>
                ))}
            </select>
            <label htmlFor={`${idPrefix}-acm-prio`}>ACM prioriteit</label>
            <select
                id={`${idPrefix}-acm-prio`}
                onChange={(event) => setAcmPrio(Number(event.target.value))}
                value={acmPrio}>
                {ACM_PRIO_OPTIONS.map((option) => (
                    <option key={option.value} value={option.value}>
                        {option.value}: {option.label}
                    </option>
                ))}
            </select>
            {error && <p className={styles.formError}>{error}</p>}
            <div className={styles.modalActions}>
                {renderAdditionalActions?.()}
                <button
                    className={styles.secondaryButton}
                    onClick={onCancel}
                    type="button">
                    Annuleer
                </button>
                <button
                    className={styles.primaryButton}
                    disabled={isSubmitting}
                    type="submit">
                    {isSubmitting ? submittingLabel : submitLabel}
                </button>
            </div>
        </form>
    );
};

export default ItemForm;
