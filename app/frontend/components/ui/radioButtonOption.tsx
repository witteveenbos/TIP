interface RadioOptions {
    label: string;
    value: string;
    icon?: string;
    selectedOption: string;
    onSelect: (value: string | boolean) => void;
}

function RadioOption({
    label,
    value,
    icon,
    selectedOption,
    onSelect,
}: RadioOptions) {
    const handleChange = () => {
        onSelect(value);
    };

    return (
        <label
            className={`cursor-pointer flex flex-row items-center justify-center p-4 m-1 rounded-md ${
                selectedOption === value
                    ? 'bg-gray-200 font-semibold'
                    : 'bg-white'
            } `}>
            {icon && <img src={icon} alt={label} className="w-6 h-6" />}
            <span className={`${icon ? 'text-xs' : 'text-sm'}`}>{label}</span>
            <input
                type="radio"
                value={value}
                checked={selectedOption === value}
                onChange={handleChange}
                className="sr-only"
            />
        </label>
    );
}

export default RadioOption;
