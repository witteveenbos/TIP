import { Button } from '@/components/ui/button';
import { useState } from 'react';
import { useAllAreasStore, useScenarioStore } from 'stores/calculateStore';
import { Combobox } from '../ui/combobox';

const SaveProvincialFutureVision = ({
    closeDialog,
    futureVisions,
    provincialFutureVision,
    setProvincialFutureVision,
    handleChange,
    handleSave,
    formErrorMessage,
}) => {
    const [filteredFutureVisions, setFilteredFutureVisions] = useState([]);
    const { allAreas } = useAllAreasStore(); // Get all areas from store
    const { scenarios } = useScenarioStore(); // Get scenarios from store

    //prepare scenario options for combobox
    const scenarioOptions = scenarios.map((scenario) => ({
        label: scenario.title,
        value: scenario.dataLink,
    }));

    //prepare region specific future visions for combobox
    const createRegionOptions = (visions) => {
        return visions.map((vision) => ({
            label: vision.name,
            value: vision.id,
        }));
    };

    // Filter future visions based on selected scenario
    function filterScenario(selectedValue) {
        const scenarioId = selectedValue;

        //save selected scenario in provincial future vision
        setProvincialFutureVision({
            ...provincialFutureVision,
            scenario: selectedValue,
        });
        //filter future visions based on selected scenario
        setFilteredFutureVisions(
            futureVisions.filter((vision) => vision.scenario === scenarioId)
        );
    }

    return (
        <div className="relative h-full">
            <form className="w-2/3">
                <div className="mb-8">
                    <div className="flex flex-col">
                        <label htmlFor="futureVisionName" className="my-1">
                            Naam provinciaal toekomstbeeld
                        </label>
                        <input
                            type="text"
                            id="provincialFutureVisionName"
                            name="name"
                            value={provincialFutureVision.name}
                            onChange={(e) =>
                                handleChange('name', e.target.value)
                            }
                            className={`shadow mt-1 appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-2 `}
                        />
                    </div>
                    <div className="flex flex-row my-4">
                        <label className="w-1/2 my-1">Scenario</label>
                        <Combobox
                            options={scenarioOptions}
                            selected={provincialFutureVision.scenario}
                            placeholder="Selecteer scenario"
                            onChange={filterScenario}
                            className="w-full"
                        />
                    </div>
                </div>
                <div>
                    {/**show an inputfield per region in the province to select a future vision for that region */}
                    {allAreas['REG'].map((region) => {
                        const areaVisions =
                            filteredFutureVisions.length > 0
                                ? filteredFutureVisions.filter(
                                      (vision) => vision.geo_id === region.gid
                                  )
                                : [];

                        return (
                            <div
                                key={region.gid}
                                className="flex flex-row my-4">
                                <label
                                    htmlFor={
                                        'provincialFutureVisionName' +
                                        region.label
                                    }
                                    className="w-1/2 my-1">
                                    {region.label}
                                </label>
                                {provincialFutureVision.scenario ? (
                                    areaVisions.length > 0 ? (
                                        <Combobox
                                            options={createRegionOptions(
                                                areaVisions
                                            )}
                                            selected={
                                                provincialFutureVision[
                                                    region.gid
                                                ]
                                            }
                                            placeholder="Selecteer een toekomstbeeld van deze regio"
                                            onChange={(value) =>
                                                handleChange(region.gid, value)
                                            }
                                            className="w-full"
                                        />
                                    ) : (
                                        <p key={region.id} className="w-full">
                                            Er zijn geen toekomstbeelden
                                            beschikbaar voor dit gebied.
                                        </p>
                                    )
                                ) : (
                                    <p className="w-full">
                                        Selecteer eerst een scenario.{' '}
                                    </p>
                                )}
                            </div>
                        );
                    })}
                </div>
            </form>
            {formErrorMessage && (
                <p className="text-red-600 font-bold">{formErrorMessage}</p>
            )}
            <div className="flex flex-row justify-end mt-12">
                <Button variant="outline" className="m-2" onClick={closeDialog}>
                    Annuleren
                </Button>
                <Button className="m-2" onClick={handleSave}>
                    Provinciaal toekomstbeeld opstellen
                </Button>
            </div>
        </div>
    );
};

export default SaveProvincialFutureVision;
