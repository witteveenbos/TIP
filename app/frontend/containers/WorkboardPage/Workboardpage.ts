export const TYPE_OPTIONS = [
    'Woningbouw',
    'Laadinfra',
    'Bedrijventerrein / logistiek',
    'Zon',
] as const;

export const STATUS_OPTIONS = [
    { value: 1, label: 'Idee (zacht)' },
    { value: 2, label: 'Beleidsvoornemen (zacht)' },
    { value: 3, label: 'Planvorming  (zacht)' },
    { value: 4, label: 'Besluitvorming loopt  (vast)' },
    { value: 5, label: 'Vastgesteld / in uitvoering (vast)' },
] as const;

export const ACM_PRIO_OPTIONS = [
    { value: 0, label: 'Geen prio' },
    { value: 1, label: 'Categorie 1: Congestieverzachters' },
    { value: 2, label: 'Categorie 2: Veiligheid' },
    { value: 3, label: 'Categorie 3: Basisbehoeften' },
] as const;

export const PHASE_CHOICES = [
    { value: 1, label: 'inzicht & invoeren', description: 'Lorem ipsum' },
    {
        value: 2,
        label: 'Samenwerksessie',
        description: 'Lorem ipsum samenwerksessie',
    },
    {
        value: 3,
        label: 'Versies vergelijken',
        description: 'In deze stap vergelijken we sessies',
    },
    {
        value: 4,
        label: 'Integraal programmeren',
        description: 'Lekker integraal programmeren',
    },
] as const;

export type ProjectType = (typeof TYPE_OPTIONS)[number];

export type SwimmingLane = {
    label: string;
    minimumEnergy: number;
    maximumEnergy: number;
    minimumRisk: number;
    maximumRisk: number;
};

export type Project = {
    id: number;
    title: string;
    description: string;
    organization: string;
    type: ProjectType;
    size_mw: number;
    acm_prio: number;
    status: number;
    user: number;
    lane: number;
    sort_order: number;
};

export type ProjectModification = {
    id: number;
    change_type: 'lane' | 'properties';
    changed_fields: string[];
    updated_at: string;
    updated_by: number | null;
    username: string | null;
};

export interface WorkboardPageProps {
    id: number;
    title?: string;
    phase?: string;
    organization?: string | null;
    isAdmin?: boolean;
    swimmingLanes?: SwimmingLane[];
}

export type ProjectDropHandler = (
    projectId: number,
    laneIndex: number,
    targetProjectId?: number,
    insertBefore?: boolean
) => void;

export interface SwimmingLaneColumnProps {
    index: number;
    lane: SwimmingLane;
    projects: Project[];
    userOrganization?: string | null;
    isAdmin?: boolean;
    phase?: string;
    canEdit: (project: Project) => boolean;
    onEdit: (project: Project) => void;
    onProjectDrop: ProjectDropHandler;
}

export interface ProjectCardProps {
    project: Project;
    canDrag: boolean;
    canEdit: boolean;
    laneIndex: number;
    onEdit: (project: Project) => void;
    onProjectDrop: ProjectDropHandler;
}

export interface CreateItemModalProps {
    isOpen: boolean;
    isSubmitting: boolean;
    error?: string;
    onClose: () => void;
    onSubmit: (
        title: string,
        description: string,
        type: ProjectType,
        sizeMw: number,
        status: number,
        acmPrio: number
    ) => void;
}

export type EditItemModalProps = CreateItemModalProps & {
    project: Project;
    onDelete: () => void;
    modifications: ProjectModification[];
    isLoadingModifications: boolean;
};
