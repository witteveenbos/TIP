import {
    useAreaDivisionStore,
    useGeoIdStore,
    useInputTypeStore,
    useScenarioStore,
} from './calculateStore';

const calculateStore = () => {
    return {
        useScenarioStore,
        useAreaDivisionStore,
        useGeoIdStore,
        useInputTypeStore,
    };
};

export default calculateStore;
