import { Button } from '@/components/ui/button';

const SavePopover = ({ save, closePopover }) => {
    return (
        <div className="flex flex-col justify-between absolute top-1/2 left-1/2 bg-white border sm:rounded-lg shadow-lg p-6 transform -translate-x-1/2 -translate-y-1/2 z-[6000] w-90 h-56">
            <p className="mb-4 text-lg text-center">
                Er bestaat al een toekomstbeeld met deze naam. Wilt u deze
                overschrijven?{' '}
            </p>
            <div className="flex flex-row justify-end">
                {' '}
                <Button
                    onClick={closePopover}
                    variant="outline"
                    className="mr-2 ">
                    Naam toekomstbeeld wijzigen
                </Button>
                <Button onClick={save}>Ja overschrijven</Button>
            </div>
        </div>
    );
};

export default SavePopover;
