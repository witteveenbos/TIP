import {
    selectedDevelopmentStore,
    useAreaDivisionStore,
    useSelectedGeoIdStore,
} from 'stores/calculateStore';

export default function EnergyBalanceZoomLevel() {
    const { areaDivision, selectedAreaDivision, setSelectedAreaDivision } =
        useAreaDivisionStore();
    const { setSelectedDevelopment } = selectedDevelopmentStore();

    const { setSelectedGeoId } = useSelectedGeoIdStore();

    function changeZoomLevel(value) {
        setSelectedAreaDivision(value);
        setSelectedDevelopment(null);
        setSelectedGeoId(null);
    }

    return (
        <div className="flex flex-col items-center justify-center">
            {areaDivision.length > 0 && (
                <fieldset>
                    <label htmlFor="ruimtelijke_indeling"></label>
                    <select
                        className="border-2 border-color-black h-8 md:h-10 rounded-md md:px-2" // Add padding here
                        onChange={(e) => changeZoomLevel(e.target.value)}
                        id="header-area-division"
                        value={selectedAreaDivision}
                        >
                        {areaDivision.map((option) => (
                            <option
                                key={option.value}
                                value={option.value}
                                className="p-2">
                                {option.label}
                            </option>
                        ))}
                    </select>
                </fieldset>
            )}
        </div>
    );
}
