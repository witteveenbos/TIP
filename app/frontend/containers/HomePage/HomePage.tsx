import EnergyBalance from '@/components/EnergyBalance';
import StartupDialog from '@/components/StartupDialog/StartupDialog';
import dynamic from 'next/dynamic';
import { useEffect, useState } from 'react';

import { getScenarios } from '@/api/api';
import { useScenarioStore } from '../../stores/calculateStore';
import { basePageWrap } from '../BasePage';

const DynamicBaseMap = dynamic(() => import('@/components/BaseMap'), {
    ssr: false,
});

export type Scenario = {
    title: string;
    description: string;
    dataLink: string;
};

interface HomePageProps {
    title: string;
}

const HomePage = (title: string) => {
    const [eindbeeld, setEindbeeld] = useState(false);
    const [loading, setLoading] = useState(false);
    const [mapLoading, setMapLoading] = useState(false);
    const { scenarios, setScenarios } = useScenarioStore();

    async function getScenariosWithAPI() {
        const scenarios = await getScenarios();
        setScenarios(scenarios);
    }

    useEffect(() => {
        if (scenarios.length === 0) {
            getScenariosWithAPI();
        }
    }, []);

    useEffect(() => {
        // Update loading state based on the mapLoading state from EnergyBalance
        if (!mapLoading) {
            handleLoading(false);
        }
    }, [mapLoading]);

    const handleLoading = (showLoading) => {
        setLoading(showLoading);
    };

    const openDialog = eindbeeld && !loading ? false : true;

    return (
        <div>
            {openDialog && (
                <>
                    <StartupDialog
                        scenarios={scenarios}
                        selectEindbeeld={setEindbeeld}
                        loading={loading}
                        handleLoading={handleLoading}
                    />
                </>
            )}
            {eindbeeld ? (
                <EnergyBalance handleMapLoading={setMapLoading} />
            ) : (
                <DynamicBaseMap />
            )}
        </div>
    );
};

export default basePageWrap(HomePage);
