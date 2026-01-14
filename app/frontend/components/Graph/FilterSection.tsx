import { Checkbox } from '../ui/checkbox';
import { FilterSectionProps } from '@/types/components/Graph';


export default function FilterSection({
    title,
    items,
    selectedItems,
    onToggleItem,
    legendData,
}: FilterSectionProps) {
    return (
        <>
            <h3 className="text-primary font-bold leading-6">{title}</h3>
            {items.map((item) => (
                <div key={item} className="relative my-1">
                    <Checkbox
                        id={item}
                        value={item}
                        defaultChecked={selectedItems.includes(item)}
                        onCheckedChange={() => onToggleItem(item)}
                    />
                    <label htmlFor={item} className="mx-4">
                        {item}
                    </label>
                    <div
                        className="absolute right-[-8px] top-1 w-4 h-4 ml-2 mr-1 border rounded border-gray-300"
                        style={{ backgroundColor: legendData[item] }}
                    />
                </div>
            ))}
        </>
    );
}