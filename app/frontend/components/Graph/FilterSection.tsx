import { Checkbox } from '../ui/checkbox';
import { FilterSectionProps } from '@/types/components/Graph';


export default function FilterSection({
    title,
    items,
    selectedItems,
    onToggleItem,
    legendData,
}: FilterSectionProps) {
    // Group items by demandSupply to show separator
    const groupedItems = items.reduce((acc, item) => {
        if (!acc[item.demandSupply]) {
            acc[item.demandSupply] = [];
        }
        acc[item.demandSupply].push(item);
        return acc;
    }, {} as Record<string, typeof items>);

    const groups = Object.entries(groupedItems);

    return (
        <>
            <h3 className="text-primary font-bold leading-6">{title}</h3>
            {groups.map(([demandSupply, groupItems], groupIndex) => (
                <div key={demandSupply}>
                    <h4>{demandSupply}</h4>
                    {groupItems.map((item) => (
                        <div key={item.name} className="relative my-1">
                            <Checkbox
                                id={item.name}
                                value={item.name}
                                defaultChecked={selectedItems.includes(item.name)}
                                onCheckedChange={() => onToggleItem(item.name)}
                            />
                            <label htmlFor={item.name} className="mx-4">
                                {item.name}
                            </label>
                            <div
                                className="absolute right-[-8px] top-1 w-4 h-4 ml-2 mr-1 border rounded border-gray-300"
                                style={{ backgroundColor: legendData[item.name] }}
                            />
                        </div>
                    ))}
                    {/* Add separator line between groups (except after the last group) */}
                    {groupIndex < groups.length - 1 && (
                        <hr className="my-2 border-t border-gray-300" />
                    )}
                </div>
            ))}
        </>
    );
}