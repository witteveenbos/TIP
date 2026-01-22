import Joyride, { CallBackProps, Placement } from 'react-joyride';
export default function Tour({
    openFutureVisionDialog,
    onClose,
}: {
    openFutureVisionDialog: () => void;
    onClose: () => void;
}) {
    const TOUR_STEPS = [
        {
            target: '#header',
            content:
                'In de bovenbalk kun je aangeven welke resultaten je wilt zien. Zoals de energiedrager, de ruimtelijke indeling en of je de originele of aangepaste data wilt zien.',
            disableBeacon: true,
        },
        {
            target: '#map',
            content:
                'Centraal staat de kaart waarop je de resultaten kunt bekijken.',
            placement: 'center' as Placement,
        },
        {
            target: '#side',
            content:
                'Met het zijpaneel kun je aannames per gemeente aanpassen en de resultaten bekijken.',
            placement: 'left' as Placement,
        },
        {
            target: '#header-area-division',
            content:
                'Hier kun je de ruimtelijke indeling aanpassen. Op gemeentelijk niveau kun je de aannames per gemeente aanpassen. Op netvlakniveau zie je de impact op het net door elektriciteit als energiedrager en vraag of aanbod als balans te selecteren. Op andere niveaus zie je geaggregeerde data maar kun je geen aanpassingen doen.',
        },
        {
            target: '#header-energycarrier',
            content:
                'Hier kies je de energiedrager die je op de kaart wilt zien. Warmte omvat restwarmte en geothermie. Onder gassen vallen waterstof en biobrandstoffen.',
        },
        {
            target: '#header-energybalance',
            content:
                'Met deze knop schakel je tussen de energiebalans, alleen energievraag of alleen energieaanbod.',
        },
        {
            target: '#header-orignal-toggle',
            content:
                'Hiermee schakel je tussen de originele data en de data waarin jouw aanpassingen zijn meegenomen.',
        },
        {
            target: '#header-menu',
            content:
                'Via het menu sla je toekomstbeelden op, laad je toekomstbeelden in of combineer je ze tot een nieuw toekomstbeeld.',
        },
        {
            target: '#side',
            content:
                "In de zijbalk doe je aanpassingen per gemeente of bekijk je gedetailleerde informatie per regio. Deze aanpassingen noemen we continue en sectorale ontwikkelingen. Selecteer een ontwikkeling en een gemeente voor het doen aanpassingen. Beweeg de muis over de verschillende regio's zonder een regio aan te klikken om informatie alleen te bekijken.",
            placement: 'left' as Placement,
        },
        {
            target: '#side-continous',
            content:
                'Continue ontwikkelingen veranderen langzaam over de tijd en kunnen niet direct door de provincie worden aangepast. Klik op een gemeente en ontwikkeling om deze aan te passen.',
            placement: 'left' as Placement,
        },
        {
            target: '#side-sectoral',
            content:
                'Sectorale ontwikkelingen zijn duidelijk te definiëren projecten waar de provincie veranderingen kan afdwingen. Klik op een gemeente en ontwikkeling om deze aan te passen. Bestaande projecten kun je aanpassen of nieuwe projecten toevoegen.',
            placement: 'left' as Placement,
        },
        {
            target: '#map',
            content:
                'Dat is het! Je bent klaar om je toekomstbeeld te gaan ontwikkelen. Succes! Neem voor vragen contact op met rob.colenbrander@witteveenbos.com.',
            placement: 'center' as Placement,
        },
    ];

    const handleJoyrideCallback = (data: CallBackProps) => {
        const { index, action, type, status } = data;

        // TODO: open the menu when reaching the menu step
        // if (type === 'step:before' && index === 7 && action === 'next') {
        //     // Open menu when reaching the menu step
        //     const menuButton = document.querySelector(
        //         '#header-menu'
        //     ) as HTMLElement;
        //     if (menuButton) {
        //         menuButton.click();
        //     }
        // }

        if (
            status === 'finished' ||
            status === 'skipped' ||
            type === 'tour:end'
        ) {
            onClose();
        }
    };
    return (
        <Joyride
            steps={TOUR_STEPS}
            continuous={true}
            showProgress={true}
            spotlightPadding={8}
            showSkipButton={true}
            disableOverlayClose={false}
            beaconComponent={null}
            run={true}
            styles={{
                options: {
                    zIndex: 2000,
                    arrowColor: '#fff',
                    backgroundColor: '#fff',
                    overlayColor: 'rgba(0, 0, 0, 0.5)',
                    primaryColor: 'hsl(208 100% 19%)',
                    textColor: 'hsl(222.2 47.4% 11.2%)',
                },
            }}
            callback={handleJoyrideCallback}
            locale={{
                back: 'Terug',
                next: 'Volgende',
                nextLabelWithProgress: 'Volgende ({step}/{steps})',
                last: 'Einde',
                open: 'Open',
                skip: 'Overslaan',
                close: 'Sluiten',
            }}
        />
    );
}
