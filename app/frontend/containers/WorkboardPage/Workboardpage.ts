export const TYPE_OPTIONS = [
    'Woningbouw',
    'Laadinfra',
    'Bedrijventerrein / logistiek',
    'Zon',
] as const;

export const STATUS_OPTIONS = [
    { value: 1, label: 'Idee' },
    { value: 2, label: 'Beleidsvoornemen' },
    { value: 3, label: 'Planvorming' },
    { value: 4, label: 'Besluitvorming loopt vast' },
    { value: 5, label: 'Vastgesteld / in uitvoering' },
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
    status: number;
    user: number;
    lane: number;
};

export interface WorkboardPageProps {
    id: number;
    title?: string;
    phase?: string;
    organization?: string | null;
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
    onProjectDrop: ProjectDropHandler;
}

export interface ProjectCardProps {
    project: Project;
    canDrag: boolean;
    laneIndex: number;
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
        status: number
    ) => void;
}
