import { Button } from '@/components/ui/button';
import { useEffect, useRef } from 'react';
import { useAllAreasStore } from 'stores/calculateStore';

const SaveFutureVision = ({
    handleFutureVisionChange,
    handleSave,
    closeDialog,
    vision,
    focusName,
}) => {
    const { allAreas } = useAllAreasStore(); // Get all areas from store
    const inputRef = useRef(null);

    useEffect(() => {
        if (focusName) {
            inputRef.current.focus();
        }
    }, [focusName]);

    function createAreaDataList() {
        return (
            <datalist
                id="regions"
                className="shadow mt-1 appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                {['PROV', 'REG'].map((key) =>
                    allAreas[key].map((item) => (
                        <option key={item.gid} value={item.label}>
                            {item.label}
                        </option>
                    ))
                )}
            </datalist>
        );
    }

    return (
        <div>
            <form>
                <div className="flex flex-row justify-between">
                    <div className="flex flex-col w-1/3 mr-4">
                        <label htmlFor="futureVisionName">
                            Benaming toekomstbeeld
                        </label>
                        <input
                            type="text"
                            id="futureVisionName"
                            name="name"
                            value={vision.name}
                            ref={inputRef}
                            onChange={handleFutureVisionChange}
                            required
                            className={`shadow mt-1 appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-2 `}
                        />
                    </div>
                    <div className="flex flex-col w-1/3 mr-4">
                        <label htmlFor="futureVisionAuthor">
                            Auteur scenario
                        </label>
                        <input
                            type="text"
                            id="futureVisionAuthor"
                            name="author"
                            required
                            value={vision.author}
                            onChange={handleFutureVisionChange}
                            className="shadow mt-1 appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-2 "
                        />
                    </div>
                    <div className="flex flex-col w-1/3 mr-4">
                        <label htmlFor="futureVisionRegion">Regio</label>
                        <input
                            list="regions"
                            id="futureVisionRegion"
                            name="geo_id"
                            onChange={handleFutureVisionChange}
                            defaultValue={vision.geo_id.label}
                            required
                            className="shadow mt-1 appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-2 "
                        />
                        {createAreaDataList()}
                    </div>
                </div>

                <div className=" mr-4 mt-4">
                    <label htmlFor="futureVisionDescription">Opmerking</label>
                    <textarea
                        id="futureVisionDescription"
                        name="description"
                        onChange={handleFutureVisionChange}
                        value={vision.description}
                        className="shadow mt-1 h-40 appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-2 "
                    />
                </div>
                <div className="flex flex-row justify-end mt-4">
                    <Button
                        variant="outline"
                        className="m-2"
                        onClick={closeDialog}>
                        Annuleren
                    </Button>
                    <Button className="m-2" onClick={handleSave}>
                        Toekomstbeeld opslaan
                    </Button>
                </div>
            </form>
        </div>
    );
};

export default SaveFutureVision;
