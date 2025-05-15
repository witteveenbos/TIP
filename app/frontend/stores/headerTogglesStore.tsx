import { create } from 'zustand';
import { createJSONStorage, devtools, persist } from 'zustand/middleware';

interface FutureVisionsDialog {
    futureVisionDialog: {
        open: boolean;
        type: 'save' | 'open' | 'combine' | 'none';
    };
    setFutureVisionDialog: (futureVisionDialog: {
        open: boolean;
        type: 'save' | 'open' | 'combine' | 'none';
    }) => void;
}

interface DragerBalanceState {
    energyCarrier: 'all' | 'electricity' | 'gas' | 'heat';
    setEnergyCarrier: (energyCarrier) => void;
    balance: 'balance' | 'demand' | 'supply';
    setBalance: (balance) => void;
    original: boolean;
    setOriginal: (original: boolean) => void;
}

export const useFutureVisionsDialogStore = create<FutureVisionsDialog>()(
    devtools(
        persist(
            (set) => ({
                futureVisionDialog: {
                    open: false,
                    type: 'none',
                },
                setFutureVisionDialog: (futureVisionDialog) =>
                    set({ futureVisionDialog }),
            }),
            {
                name: 'future-visions-dialog-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);

export const useDragersStore = create<DragerBalanceState>()(
    devtools(
        persist(
            (set) => ({
                energyCarrier: 'all',
                setEnergyCarrier: (energyCarrier) => set({ energyCarrier }),
                balance: 'balance',
                setBalance: (balance) => set({ balance }),
                original: false,
                setOriginal: (original: boolean) => set({ original }),
            }),
            {
                name: 'dragers-store',
                storage: createJSONStorage(() => sessionStorage),
            }
        )
    )
);
