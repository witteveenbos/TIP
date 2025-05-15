import { XMarkIcon } from '@heroicons/react/24/outline';
import { useEffect, useState } from 'react';
import {
    continuousDevelopmentsChangesStore,
    sectoralDevelopmentsChangesStore,
    useAllAreasStore,
    useAreaDivisionStore,
    useMunicipalityScenariosStore,
} from 'stores/calculateStore';
import {
    combineFutureVisions,
    getFutureVision,
    getFutureVisions,
    postFutureVision,
    putFutureVision,
} from '../../api/api';
import Loader from '../Loader/Loader';
import { Dialog, DialogOverlay } from '../ui/dialog';
import OpenFutureVision from './OpenFutureVision';
import SaveFutureVision from './SaveFutureVision';
import SavePopover from './SavePopover';
import SaveProvincialFutureVision from './SaveProvincialFutureVision';

const FutureVisionDialog = ({
    closeDialog,
    dialogType,
    scenario,
    changeZoomLevel,
}) => {
    const [futureVision, setFutureVision] = useState({
        name: '',
        author: '',
        geo_id: {
            gid: '',
            label: '',
        },
        description: '',
        json_data: {},
        scenario: scenario,
    });
    const { changedContinuousDevelopments, setChangedContinuousDevelopments } =
        continuousDevelopmentsChangesStore();
    const { changedSectoralDevelopments, setChangedSectoralDevelopments } =
        sectoralDevelopmentsChangesStore();
    const { allAreas } = useAllAreasStore();
    const { setSelectedAreaDivision } = useAreaDivisionStore();
    const { municipalityScenarios, setMunicipalityScenarios } =
        useMunicipalityScenariosStore();
    const [futureVisions, setFutureVisions] = useState(null);
    const [provincialFutureVision, setProvincialFutureVision] = useState({
        geo_id: allAreas['PROV'][0].gid,
    });
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const [formErrorMessage, setFormErrorMessage] = useState('');
    const [loader, setLoader] = useState(false);
    const [showPopover, setShowPopover] = useState(false);
    const [focusName, setFocusName] = useState(false);

    let titleDialog;

    useEffect(() => {
        allFutureVisions();
    }, [dialogType]);

    const handleFutureVisionChange = (e) => {
        e.preventDefault();
        if (e.target.name === 'geo_id') {
            const selectedItem = Object.values(allAreas)
                .flat()
                .find((item) => item.label === e.target.value);
            if (selectedItem) {
                setFutureVision({
                    ...futureVision,
                    geo_id: selectedItem.gid, // Save the value (item.gid)
                });
            }
        } else {
            setFutureVision({
                ...futureVision,
                [e.target.name]: e.target.value,
            });
        }
    };

    const handleSaveFutureVision = (e) => {
        e.preventDefault();

        //prepareFutureVision with data for saving
        const futureVisionSave = {
            ...futureVision,
        };
        if (futureVision.geo_id.gid) {
            futureVisionSave.geo_id = futureVision.geo_id.gid;
        }
        const combinedDevelopments = changedContinuousDevelopments.concat(
            changedSectoralDevelopments
        );
        //hier municipalitiesScenarios toevoegen
        const newFutureVision = {
            developments: combinedDevelopments,
            municipalitiesScenarios: municipalityScenarios,
        };
        futureVisionSave.json_data = JSON.stringify(newFutureVision);
        //check if future vision already exists.
        if (checkUniqueName(futureVisionSave.name)) {
            //if not post future vision
            postFutureVision(futureVisionSave).then((response) => {
                if (response.name !== undefined) {
                    setSuccessMessage('Toekomstbeeld opgeslagen');
                    //reset changes
                    setChangedContinuousDevelopments([]);
                    setChangedSectoralDevelopments([]);
                } else {
                    setErrorMessage(
                        'Er is iets mis gegaan, probeer het later opnieuw'
                    );
                }
            });
        } else {
            //if future vision already exists check if need to be overwritten
            setShowPopover(true);
        }
    };

    const handleChangeFutureVision = (e) => {
        e.preventDefault();
        putFutureVision(futureVision).then((response) => {
            if (response.name !== undefined) {
                setSuccessMessage('Toekomstbeeld aangepast');
                //reset changes
                setChangedContinuousDevelopments([]);
                setChangedSectoralDevelopments([]);
            } else {
                setErrorMessage(
                    'Er is iets mis gegaan, probeer het later opnieuw'
                );
            }
        });
        setShowPopover(false);
    };

    const handleProvincialFutureVisionChange = (key, value) => {
        setFormErrorMessage('');
        setProvincialFutureVision({
            ...provincialFutureVision,
            [key]: value,
        });
    };

    const handleSaveProvincialFutureVision = (e) => {
        e.preventDefault();

        //check if name is entered
        if (!provincialFutureVision.name) {
            setFormErrorMessage('Vul een naam in');
            return;
        }
        //
        //prepareProvincialFutureVision with data for saving- no empty regional keys
        const cleanProvincialFutureVision = Object.fromEntries(
            Object.entries(provincialFutureVision).filter(([key, value]) => {
                // Check if the key includes "REG" and the value is not empty or undefined
                return (
                    !key.includes('REG') ||
                    (value !== '' && value !== undefined)
                );
            })
        );

        combineFutureVisions(cleanProvincialFutureVision).then((response) => {
            if (response.name !== undefined) {
                setSuccessMessage('Provinciaal toekomstbeeld opgeslagen');
                setProvincialFutureVision({});
                //open newly created provincial future vision
                openFutureVision(response.id);
                //set regional division
                setSelectedAreaDivision('REG');
                changeZoomLevel(9); //zoom to provincial level
            } else {
                setErrorMessage(
                    'Er is iets mis gegaan, probeer het later opnieuw'
                );
            }
        });
    };

    const allFutureVisions = () => {
        getFutureVisions().then((response) => {
            if (response) {
                setFutureVisions(response);
            } else {
                setErrorMessage(
                    'Er is iets mis gegaan, probeer het later opnieuw'
                );
            }
        });
    };

    const openFutureVision = (id) => {
        setLoader(true);
        getFutureVision(id).then((response) => {
            if (response) {
                const parsedJson = JSON.parse(response.json_data);
                //split continuous and sectoral developments
                const { sectoralDevelopment, continuousDevelopments } =
                    parsedJson.developments.reduce(
                        (acc, obj) => {
                            if (obj.hasOwnProperty('projectId')) {
                                acc.sectoralDevelopment.push(obj);
                            } else {
                                acc.continuousDevelopments.push(obj);
                            }
                            return acc;
                        },
                        { sectoralDevelopment: [], continuousDevelopments: [] }
                    );
                setChangedContinuousDevelopments(continuousDevelopments); //load continuousdevelopments from future vision
                setChangedSectoralDevelopments(sectoralDevelopment); //load sectoraldevelopments from future vision
                setMunicipalityScenarios(parsedJson.municipalitiesScenarios); //load municipalityScenarios from future vision
                setLoader(false);
                setSuccessMessage('Je toekomstbeeld is geladen.');
            } else {
                setLoader(false);
                setErrorMessage(
                    'Er is iets mis gegaan, probeer het later opnieuw'
                );
            }
        });
    };

    const checkUniqueName = (name) => {
        if (futureVisions) {
            const names = futureVisions.map((item) => item.name);
            if (names.includes(name)) {
                //if name is already in use the id is saved in the futureVision object
                const foundID = futureVisions.find(
                    (item) => item.name === name
                ).id;
                setFutureVision((prev) => ({ ...prev, id: foundID }));
                return false;
            } else {
                return true;
            }
        }
    };

    const createTitleDialog = () => {
        if (dialogType === 'save') {
            titleDialog = 'Toekomstbeeld opslaan';
        } else if (dialogType === 'open') {
            titleDialog = 'Toekomstbeeld openen';
        } else if (dialogType === 'combine') {
            titleDialog = 'Provinciaal toekomstbeeld';
        } else {
            return '';
        }
    };
    createTitleDialog();

    const handleClosePopover = () => {
        setShowPopover(false);
        setFocusName(true);
    };

    return (
        <Dialog open>
            <DialogOverlay className="DialogOverlay" id="future_vision_dialog">
                <div className="fixed h-[90%] left-[50%] top-[50%] z-[5000] grid w-[90%] translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-8 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg overflow-y-auto">
                    <div className="StartupDialog__step2 flex flex-col relative">
                        <div className="flex flex-row items-center justify-between mb-4">
                            <h2>{titleDialog}</h2>
                            <button onClick={() => closeDialog()}>
                                <XMarkIcon className="h-10 w-10"></XMarkIcon>
                            </button>
                        </div>
                        {showPopover && (
                            <SavePopover
                                save={handleChangeFutureVision}
                                closePopover={handleClosePopover}
                            />
                        )}
                        {loader ? (
                            <div className="flex flex-col items-center justify-center">
                                <Loader />
                                <p>Toekomstbeeld wordt geladen...</p>
                            </div>
                        ) : successMessage ? (
                            <p>{successMessage}</p>
                        ) : errorMessage ? (
                            <p>{errorMessage}</p>
                        ) : dialogType === 'save' ? (
                            <SaveFutureVision
                                handleFutureVisionChange={
                                    handleFutureVisionChange
                                }
                                vision={futureVision}
                                handleSave={handleSaveFutureVision}
                                closeDialog={closeDialog}
                                focusName={focusName}
                            />
                        ) : dialogType === 'open' && futureVisions ? (
                            <OpenFutureVision
                                futureVisions={futureVisions}
                                openFutureVision={openFutureVision}
                            />
                        ) : dialogType === 'combine' && futureVisions ? (
                            // Add your desired JSX component here
                            <SaveProvincialFutureVision
                                closeDialog={closeDialog}
                                futureVisions={futureVisions}
                                provincialFutureVision={provincialFutureVision}
                                handleChange={
                                    handleProvincialFutureVisionChange
                                }
                                handleSave={handleSaveProvincialFutureVision}
                                setProvincialFutureVision={
                                    setProvincialFutureVision
                                }
                                formErrorMessage={formErrorMessage}
                            />
                        ) : null}
                    </div>
                </div>
            </DialogOverlay>
        </Dialog>
    );
};

export default FutureVisionDialog;
