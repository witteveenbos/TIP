import { CheckIcon, ChevronUpDownIcon } from '@heroicons/react/24/outline';
import { useState } from 'react';

import { cn } from '../../utils/cn';
import { Button } from './button';
import {
    Command,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from './command';
import { Popover, PopoverContent, PopoverTrigger } from './popover';
import { ScrollArea } from './scroll-area';

export type ComboboxOptions = {
    value: string;
    label: string;
};

interface ComboboxProps {
    options: ComboboxOptions[];
    selected: string | string[]; // Updated to handle multiple selections
    className?: string;
    placeholder?: string;
    onChange?: (event: string | string[]) => void; // Updated to handle multiple selections
}

export function Combobox({
    options,
    selected,
    className,
    placeholder,
    onChange,
}: ComboboxProps) {
    const [open, setOpen] = useState(false);
    const [query, setQuery] = useState<string>('');

    const handleSelect = (currentValue: string) => {
        if (selected === currentValue) {
            onChange('');
        } else {
            onChange(currentValue);
        }
        setOpen(false);
    };

    const filteredOptions = options.filter((option) =>
        option.label.toLowerCase().includes(query.toLowerCase())
    );

    return (
        <div className={cn('block', className)}>
            <Popover open={open} onOpenChange={setOpen}>
                <PopoverTrigger asChild>
                    <Button
                        key={'combobox-trigger'}
                        type="button"
                        variant="outline"
                        role="combobox"
                        aria-expanded={open}
                        className="w-full justify-between">
                        {selected ? (
                            <div className="relative mr-auto flex flex-grow flex-wrap items-center overflow-hidden">
                                <span>
                                    {
                                        options.find(
                                            (item) => item.value === selected
                                        )?.label
                                    }
                                </span>
                            </div>
                        ) : (
                            placeholder ?? 'Select Item...'
                        )}

                        <ChevronUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                    </Button>
                </PopoverTrigger>
                <PopoverContent className="w-72 max-w-sm p-0">
                    <Command>
                        <CommandInput
                            placeholder={placeholder ?? 'Search Item...'}
                            value={query}
                            onValueChange={(value: string) => setQuery(value)}
                        />
                        <ScrollArea>
                            <div className="max-h-80">
                                <CommandGroup>
                                    <CommandList>
                                        {filteredOptions.map((option) => (
                                            <CommandItem
                                                key={option.value}
                                                value={option.value}
                                                onSelect={() =>
                                                    handleSelect(option.value)
                                                }>
                                                <CheckIcon
                                                    className={cn(
                                                        'mr-2 h-4 w-4',
                                                        Array.isArray(selected)
                                                            ? selected.includes(
                                                                  option.value
                                                              )
                                                                ? 'opacity-100'
                                                                : 'opacity-0'
                                                            : selected ===
                                                                option.value
                                                              ? 'opacity-100'
                                                              : 'opacity-0'
                                                    )}
                                                />
                                                {option.label}
                                            </CommandItem>
                                        ))}
                                    </CommandList>
                                </CommandGroup>
                            </div>
                        </ScrollArea>
                    </Command>
                </PopoverContent>
            </Popover>
        </div>
    );
}
