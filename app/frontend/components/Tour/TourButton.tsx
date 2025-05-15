import { Button } from '@/components/ui/button';
import { Info } from 'lucide-react';
import { useState } from 'react';
import { useFutureVisionsDialogStore } from 'stores/headerTogglesStore';
import Tour from './Tour';

export default function TourButton() {
    const [isTourActive, setIsTourActive] = useState(false);

    const { setFutureVisionDialog } = useFutureVisionsDialogStore();

    const openFutureVisionDialog = () => {
        setFutureVisionDialog({
            open: true,
            type: 'open',
        });
    };

    return (
        <>
            <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsTourActive(true)}
                aria-label="Start tour">
                <Info className="h-6 w-6" />
            </Button>
            {isTourActive && (
                <Tour
                    openFutureVisionDialog={openFutureVisionDialog}
                    onClose={() => setIsTourActive(false)}
                />
            )}
        </>
    );
}
