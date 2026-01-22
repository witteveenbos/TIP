import { Scenario } from '@/containers/HomePage/HomePage';
import { InformationCircleIcon } from '@heroicons/react/24/outline';
import { Popover, PopoverContent, PopoverTrigger } from '../ui/popover';

interface StartupDialogButtonProps {
    index: string;
    scenario: Scenario;
    handleSelectScenario: (scenario: string) => void;
}

export default function StartupDialogButton({
    scenario,
    index,
    handleSelectScenario,
}: StartupDialogButtonProps) {
    return (
        <div
            className="h-20 bg-secondary  mt-2 flex flex-row justify-between px-5"
            key={index}>
            <button
                onClick={() => handleSelectScenario(scenario.dataLink)}
                value={scenario.title}
                className="flex flex-row items-center w-full h-full">
                <h2 className="ml-5">{scenario.title}</h2>
            </button>
            <Popover>
                <PopoverTrigger className="relative">
                    <InformationCircleIcon className="h-8 w-8 hover:fill-primary hover:stroke-white "></InformationCircleIcon>
                </PopoverTrigger>
                <PopoverContent side="left">
                    <div className="p-4">
                        <h3>{scenario.title}</h3>
                        <p>{scenario.description}</p>
                    </div>
                </PopoverContent>
            </Popover>
        </div>
    );
}
