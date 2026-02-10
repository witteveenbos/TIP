import { GraphProps } from '@/types/components/Graph';

export default function EnergyProfileGraph({ data }: GraphProps) {
    return (
        <div className="flex flex-col max-h-[550px] flex-1">
            <div className="text-center p-8">
                <h3 className="text-lg font-semibold mb-4">Energie Profiel</h3>
                <p className="text-gray-600">Energie profiel grafiek komt hier...</p>
            </div>
        </div>
    );
}
