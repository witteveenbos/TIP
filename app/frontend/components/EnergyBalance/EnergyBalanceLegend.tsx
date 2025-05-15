import L from 'leaflet';
import { useEffect } from 'react';
import s from './EnergyBalance.module.css';

export default function EnergyBalanceLegend({
    map,
    colors,
    labels,
    title,
    unit,
    metadata,
    selectedDevelopment,
}) {
    useEffect(() => {
        if (map && map.current) {
            // Remove any existing legend
            const existingLegend = document.querySelector(
                '.' + s.EnergyBalanceLegend
            );
            if (existingLegend) {
                existingLegend.remove();
            }

            // Create new legend
            if (metadata !== null || selectedDevelopment !== null) {
                const legend = L.control({ position: 'bottomleft' });
                legend.onAdd = () => {
                    const div = L.DomUtil.create('div', s.EnergyBalanceLegend);
                    let legendHTML = '';

                    for (let i = 0; i < colors.length; i++) {
                        legendHTML +=
                            '<li><span style="background:' +
                            colors[i] +
                            '"></span>' +
                            labels[i] +
                            (unit ? ' ' + unit : '') +
                            '</li>';
                    }

                    div.innerHTML = `<h2>${title}</h2><ul>${legendHTML}</ul>`;
                    return div;
                };

                // Add new legend to the map
                legend.addTo(map.current);
            }
        }
    }, [map, title, metadata, selectedDevelopment]);

    return null;
}
