import { ChevronDown, ChevronUp, FolderOpen, Save } from 'lucide-react';
import { useState } from 'react';
import { useFutureVisionsDialogStore } from 'stores/headerTogglesStore';

import TourButton from '../Tour/TourButton';
import { Button } from '../ui/button';
const Navbar = () => {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const { futureVisionDialog, setFutureVisionDialog } =
        useFutureVisionsDialogStore();

    const toggleDropdown = () => {
        setIsDropdownOpen(!isDropdownOpen);
    };

    const toggleFutureVisionView = (type) => {
        setFutureVisionDialog({
            open: true,
            type: futureVisionDialog.open ? 'none' : type,
        });
        toggleDropdown();
    };

    const symbol = isDropdownOpen ? (
        <ChevronUp size={16} />
    ) : (
        <ChevronDown size={16} />
    );

    return (
        <nav className="p-4 relative">
            <ul className="flex items-center gap-2">
                <li>
                    <TourButton />
                </li>
                <li>
                    <div className="flex items-center" id="header-menu">
                        <Button
                            className=""
                            onClick={toggleDropdown}
                            variant="ghost">
                            {symbol} Menu
                        </Button>

                        {isDropdownOpen && (
                            <div className="absolute  bg-white p-2 rounded shadow-md z-[1800] top-16 h-96 right-0 w-96 ">
                                <div className="flex flex-row justify-center mt-4 flex-wrap gap-2">
                                    <Button
                                        className=""
                                        onClick={() =>
                                            toggleFutureVisionView('save')
                                        }>
                                        Opslaan als{' '}
                                        <Save
                                            color="#FFF"
                                            size={16}
                                            className="ml-2"
                                        />
                                    </Button>
                                    <Button
                                        className=""
                                        onClick={() =>
                                            toggleFutureVisionView('open')
                                        }>
                                        Openen{' '}
                                        <FolderOpen
                                            color="#FFF"
                                            size={16}
                                            className="ml-2"
                                        />
                                    </Button>
                                    <Button
                                        className="mt-2"
                                        onClick={() =>
                                            toggleFutureVisionView('combine')
                                        }>
                                        Toekomstbeelden combineren
                                        <FolderOpen
                                            color="#FFF"
                                            size={16}
                                            className="ml-2"
                                        />
                                    </Button>
                                </div>
                            </div>
                        )}
                    </div>
                </li>
            </ul>
        </nav>
    );
};

export default Navbar;
