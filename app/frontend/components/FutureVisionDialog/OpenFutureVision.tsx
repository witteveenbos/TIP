import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';

const OpenFutureVision = ({ futureVisions, openFutureVision }) => {
    const headers = [
        'Scenario',
        'Regio',
        'Benaming',
        'Auteur',
        'Datum',
        'Opmerking',
    ];

    const handleRowClick = (index) => {
        openFutureVision(index);
    };

    function formatDate(dateString) {
        const dateObj = new Date(dateString);
        const day = dateObj.getDate();
        const month = dateObj.getMonth() + 1;
        const year = dateObj.getFullYear();
        return `${(day < 10 ? '0' : '') + day}-${(month < 10 ? '0' : '') + month}-${year}`;
    }

    if (!futureVisions || futureVisions.length === 0) {
        return <p>Er zijn geen toekomstbeelden beschikbaar.</p>;
    }

    return (
        <div className="">
            <Table>
                <TableHeader>
                    <TableRow>
                        {headers.map((header) => (
                            <TableHead key={header}>{header}</TableHead>
                        ))}
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {futureVisions.map((item, index) => {
                        const formattedDate = formatDate(item.created_at);
                        return (
                            <TableRow
                                key={index}
                                onClick={() => handleRowClick(item.id)}
                                className="cursor-pointer">
                                <TableCell>{item.scenario}</TableCell>
                                <TableCell>{item.geo_id_label}</TableCell>
                                <TableCell>{item.name}</TableCell>
                                <TableCell>{item.author}</TableCell>
                                <TableCell>{formattedDate}</TableCell>
                                <TableCell className="line-clamp-1 h-10">
                                    {item.description}
                                </TableCell>
                            </TableRow>
                        );
                    })}
                </TableBody>
            </Table>{' '}
        </div>
    );
};

export default OpenFutureVision;
