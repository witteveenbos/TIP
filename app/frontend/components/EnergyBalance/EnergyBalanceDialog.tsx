import { XMarkIcon } from '@heroicons/react/24/outline';
import { useState } from 'react';
import EnergyBalanceGraph from '../Graph/EnergyBalanceGraph';
import EnergyProfileGraph from '../Graph/EnergyProfileGraph';
import { Dialog, DialogOverlay } from '../ui/dialog';
import RadioOption from '../ui/radioButtonOption';

interface EnergyBalanceDialogProps {
    graphData: any;
    region: any;
    closeDialog: () => void;
}

export default function EnergyBalanceDialog({
    graphData,
    region,
    closeDialog,
}: EnergyBalanceDialogProps) {
    const [activeTab, setActiveTab] = useState<'balance' | 'profile'>('balance');

    return (
        <Dialog open>
            <DialogOverlay className="DialogOverlay">
                <div className="fixed h-[90%] left-[50%] top-[50%] z-[5000] flex flex-col w-[90%] translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state:closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state:closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state:closed]:slide-out-to-left-1/2 data-[state:closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg">
                    <div className="flex-1 overflow-y-auto p-6">
                        {/* Header with tabs */}
                        <div className="flex flex-row items-center justify-between mb-4">
                            <div className="flex items-center justify-between gap-6 w-full mr-8">
                                <h2>{region?.label}</h2>
                                <div className="flex">
                                    <RadioOption
                                        label="Energiebalans"
                                        value="balance"
                                        selectedOption={activeTab}
                                        onSelect={(value) => setActiveTab(value as 'balance' | 'profile')}
                                    />
                                    <RadioOption
                                        label="Energieprofiel"
                                        value="profile"
                                        selectedOption={activeTab}
                                        onSelect={(value) => setActiveTab(value as 'balance' | 'profile')}
                                    />
                                </div>
                            </div>
                            <button onClick={closeDialog}>
                                <XMarkIcon className="h-10 w-10"></XMarkIcon>
                            </button>
                        </div>
                        
                        {/* Tab content */}
                        {graphData !== null ? (
                            <div>
                                {activeTab === 'balance' && (
                                    <EnergyBalanceGraph data={graphData} scenario="" />
                                )}
                                {activeTab === 'profile' && (
                                    <EnergyProfileGraph 
                                        enabled={activeTab === 'profile'} 
                                    />
                                )}
                            </div>
                        ) : (
                            <p>
                                Er is helaas geen grafiek beschikbaar.{' '}
                            </p>
                        )}
                    </div>
                </div>
            </DialogOverlay>
        </Dialog>
    );
}
