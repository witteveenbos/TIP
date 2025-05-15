import { useDragersStore } from 'stores/headerTogglesStore';
import { Input } from '../ui/input';
import s from './EnergyBalance.module.css';

type DevelopmentProps = {
    gid: number;
    saveInput: (e: any, projectId?: number) => void;
    developmentInput: {
        key?: string;
        name?: string;
        default?: number;
        min?: number;
        max?: number;
        unit: string;
        disabled?: boolean;
        devKey?: string; // Added to handle projectId case
        value?: string; // Added to handle projectId case
    };
    developmentKey: string;
    developmentType: 'continuous' | 'sectoral';
    changedDevelopments: any[];
    selectedDevelopment: any;
    selectedAreaDivision: string;
    projectId?: number;
};

export default function Development({
    gid,
    saveInput,
    developmentInput,
    developmentKey,
    developmentType,
    changedDevelopments,
    selectedDevelopment,
    selectedAreaDivision,
    projectId,
}: DevelopmentProps) {
    const { original } = useDragersStore();
    function getDefaultValue(development) {
        let changedDevelopment;

        // If the user has set the toggle to 'Original', return the default value of the development
        if (original) {
            if (projectId) {
                return development.value;
            } else {
                return development.default;
            }
        }

        // If projectId is passed, it is a changed (sectoral) development -> find the changed development by projectId
        if (projectId) {
            changedDevelopment = changedDevelopments.find(
                (dev) =>
                    dev.municipalityID === gid &&
                    dev.devGroupKey === developmentKey &&
                    dev.projectId === projectId
            );
            // If it is a continuous dev, check if it is changed
        } else if (changedDevelopments) {
            changedDevelopment = changedDevelopments.find(
                (dev) =>
                    dev.municipalityID === gid &&
                    dev.devGroupKey === developmentKey
            );
        }

        // If changedDevelopment is found, return the changed value
        if (changedDevelopment) {
            const change = changedDevelopment.changes.find(
                (change) =>
                    change.devKey === development.devKey ||
                    change.devKey === development.key
            );
            return change ? change.value : development.default;
            // If no changedDevelopment is found, return the default value for continuous developments and the min value for sectoral
        } else {
            if (developmentType === 'sectoral') {
                return development.min;
            } else {
                return development.default;
            }
        }
    }

    // Debounce the input to save the input after the user has stopped typing
    const processChange = debounce((event) => saveInput(event, projectId));

    function debounce(func, timeout = 1600) {
        let timer;
        return (...args) => {
            clearTimeout(timer);
            timer = setTimeout(() => {
                func.apply(this, args);
            }, timeout);
        };
    }

    return (
        <div className={`${s.ButtonWithSwitch__details__left}`}>
            {developmentInput.name && (
                <label className="flex-[1_0_40%] w-2/5 text-white text-sm ">
                    {developmentInput.name}
                </label>
            )}
            <Input
                onClick={(e) => {
                    (developmentInput.devKey || developmentInput.key) &&
                        selectedDevelopment?.key ==
                            (developmentInput.devKey || developmentInput.key) &&
                        e.stopPropagation();
                }}
                data-develop-input={
                    developmentInput.devKey || developmentInput.key
                }
                onInput={(e) => processChange(e)}
                type="number"
                key={Math.round(getDefaultValue(developmentInput))}
                defaultValue={Math.round(getDefaultValue(developmentInput))}
                disabled={selectedAreaDivision !== 'GM'}
                className={
                    `flex-[1_0_40%] w-[] ` +
                    (changedDevelopments
                        ?.filter((cd: any) => cd.municipalityID === gid)
                        .map((dev) => dev.changes)
                        .flat()
                        .filter(
                            (dev) =>
                                dev.devKey ==
                                (developmentInput.devKey ||
                                    developmentInput.key)
                        ).length > 0 && ' border-4  ') +
                    (developmentInput.disabled
                        ? ' pointer-events-none bg-none group-hover:text-white group-active:text-white'
                        : '')
                }
                min={developmentInput.min}
                max={developmentInput.max}
                step="1"
            />
            <span className="flex-[0_0_10%] w-1/5">
                {developmentInput.unit}
            </span>
        </div>
    );
}
