import Link from 'next/link';
import { useDragersStore } from 'stores/headerTogglesStore';
import alledragers from '../../public/img/icon-alle-dragers.svg';
import energie from '../../public/img/icon-elektriciteit.svg';
import gassen from '../../public/img/icon-gassen.svg';
import warmte from '../../public/img/icon-warmte.svg';
import RadioOption from '../ui/radioButtonOption';
import EnergyBalanceZoomLevel from './EnergyBalanceZoomLevel';
import Navbar from './Navbar';

interface Logo {
    url: string;
}

interface HeaderProps {
    logo?: Logo;
}

const Header = ({ logo }: HeaderProps) => {
    const {
        energyCarrier,
        setEnergyCarrier,
        balance,
        setBalance,
        original,
        setOriginal,
    } = useDragersStore();
    const originalLabel = original ? 'Origineel' : 'Aangepast';

    const toggleOriginal = (value) => {
        if (value === 'Origineel') {
            setOriginal(true);
        } else {
            setOriginal(false);
        }
    };

    return (
        <header>
            <div className="flex flex-row justify-between h-16" id="header">
                <div className="flex flex-row items-center">
                    {logo && (
                        <Link href="/">
                            {/* eslint-disable-next-line @next/next/no-img-element */}
                            <img
                                src={logo.url}
                                alt="logo with link to homepage"
                                className="max-h-14 mx-2.5 my-1"
                                width={150}
                                height={150}
                            />
                        </Link>
                    )}
                </div>

                <div className="flex flex-row justify-start">
                    <EnergyBalanceZoomLevel />
                    <div
                        className="flex flex-row justify-between border-gray-200 rounded-md border-[0.5px] m-2"
                        id="header-energycarrier">
                        <RadioOption
                            label="Alle dragers"
                            icon={alledragers.src}
                            value="all"
                            selectedOption={energyCarrier}
                            onSelect={setEnergyCarrier}
                        />
                        <RadioOption
                            label="Elektriciteit"
                            value="electricity"
                            icon={energie.src}
                            selectedOption={energyCarrier}
                            onSelect={setEnergyCarrier}
                        />
                        <RadioOption
                            label="Warmte"
                            value="heat"
                            icon={warmte.src}
                            selectedOption={energyCarrier}
                            onSelect={setEnergyCarrier}
                        />
                        <RadioOption
                            label="Gassen"
                            value="gas"
                            icon={gassen.src}
                            selectedOption={energyCarrier}
                            onSelect={setEnergyCarrier}
                        />
                    </div>
                    <div
                        className="flex flex-row justify-between border-gray-200 rounded-md border-[0.5px] m-2"
                        id="header-energybalance">
                        <RadioOption
                            label="Balans"
                            value="balance"
                            selectedOption={balance}
                            onSelect={setBalance}
                        />
                        <RadioOption
                            label="Vraag"
                            value="demand"
                            selectedOption={balance}
                            onSelect={setBalance}
                        />
                        <RadioOption
                            label="Aanbod"
                            value="supply"
                            selectedOption={balance}
                            onSelect={setBalance}
                        />
                    </div>
                    <div
                        className="flex flex-row justify-between border-gray-200 rounded-md border-[0.5px] m-2"
                        id="header-orignal-toggle">
                        <RadioOption
                            label="Origineel"
                            value="Origineel"
                            selectedOption={originalLabel}
                            onSelect={toggleOriginal}
                        />
                        <RadioOption
                            label="Aangepast"
                            value="Aangepast"
                            selectedOption={originalLabel}
                            onSelect={toggleOriginal}
                        />
                    </div>
                </div>
                <div className="flex items-center">
                    <Navbar />
                </div>
            </div>
        </header>
    );
};

export default Header;
