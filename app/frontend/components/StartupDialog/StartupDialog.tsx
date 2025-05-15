import { ArrowLeftIcon } from '@heroicons/react/24/outline';
import { useState } from 'react';
import { useScenarioStore } from 'stores/calculateStore';
import { getMainGraph } from '../../api/api';
import { Scenario } from '../../containers/HomePage/HomePage';
import Graph from '../Graph/Graph';
import Loader from '../Loader/Loader';
import { Button } from '../ui/button';
import { Dialog, DialogOverlay } from '../ui/dialog';

import StartupDialogButton from './StartupDialogButton';

interface StartupDialogProps {
    scenarios: Scenario[];
    selectEindbeeld: React.Dispatch<React.SetStateAction<boolean>>;
    loading: boolean;
    handleLoading: (showLoading: boolean) => void;
}

export default function StartupDialog({
    scenarios,
    selectEindbeeld,
    loading,
    handleLoading,
}: StartupDialogProps) {
    const [showStep, setShowStep] = useState(1);
    const [graphData, setGraphData] = useState(null);
    const [graphDataLoading, setGraphLoading] = useState(false);
    const { selectedScenario, setSelectedScenario } = useScenarioStore();
    const [error, setError] = useState(null);

    const handleSelectScenario = (scenario: string) => {
        setSelectedScenario(scenario);
        setGraphLoading(true);

        getMainGraph(scenario).then((res) => {
            setGraphData(null);
            if (res.graph) {
                setGraphLoading(false);
                setGraphData(res);
                setShowStep(2);
            } else {
                setShowStep(2);
                setGraphLoading(false);
                setError(
                    'Er is helaas iets misgegaan bij het ophalen van de grafiek. Ga door naar het eindbeeld om met de tool te werken.'
                );
            }
        });
        setShowStep(2);
    };

    const handleBack = () => {
        setError(null);
        setShowStep(1);
    };

    const handleSelectEindbeeld = (e) => {
        e.preventDefault();
        handleLoading(true);
        selectEindbeeld(true);
    };

    return (
        <Dialog open>
            <DialogOverlay className="DialogOverlay">
                <div className="fixed h-[90%] left-[50%] top-[50%] z-[5000] grid w-[90%] translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state:closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state:closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state:closed]:slide-out-to-left-1/2 data-[state:closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg overflow-y-auto">
                    {loading ? (
                        <div className="flex flex-col items-center justify-center">
                            <Loader />
                            <p>Instellingen worden geladen...</p>
                        </div>
                    ) : selectedScenario === '' || showStep === 1 ? (
                        <div className="StartupDialog__step1 relative">
                            <div className="flex flex-row mb-4">
                                <div className="hidden mr-4">
                                    <ArrowLeftIcon className="h-8 w-8"></ArrowLeftIcon>
                                </div>
                                <div>
                                    <p>Provincie</p>
                                    <h2>Kies een standaard eindbeeld</h2>
                                </div>
                            </div>
                            <div>
                                {scenarios.length !== 0 &&
                                    scenarios.map((scen) => {
                                        return (
                                            <StartupDialogButton
                                                scenario={scen}
                                                key={scen.title}
                                                index={scen.title}
                                                handleSelectScenario={
                                                    handleSelectScenario
                                                }
                                            />
                                        );
                                    })}
                            </div>
                        </div>
                    ) : (
                        showStep === 2 && (
                            <div className="StartupDialog__step2 flex flex-col">
                                {graphDataLoading && (
                                    <div className="absolute z-30 top-0 left-0 w-full h-full flex flex-col justify-center items-center bg-white bg-opacity-80">
                                        <Loader /> Grafiek data laden...
                                    </div>
                                )}

                                <div className="flex flex-row items-center mb-4">
                                    <button onClick={handleBack}>
                                        <ArrowLeftIcon className="h-10 w-10"></ArrowLeftIcon>
                                    </button>
                                    <div className="ml-4">
                                        <h2>Eindbeeld {selectedScenario}</h2>
                                    </div>
                                </div>
                                {error && <p>{error}</p>}
                                {graphData && (
                                    <Graph
                                        data={graphData}
                                        scenario={selectedScenario}
                                    />
                                )}

                                <div className="flex flex-row justify-end w-[90%] fixed bottom-2">
                                    <Button onClick={handleSelectEindbeeld}>
                                        Selecteren eindbeeld
                                    </Button>
                                </div>
                            </div>
                        )
                    )}
                </div>
            </DialogOverlay>
        </Dialog>
    );
}
