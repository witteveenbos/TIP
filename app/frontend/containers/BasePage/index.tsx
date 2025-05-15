import React from 'react';
import BasePage from './BasePage';

export function basePageWrap<P extends object>(
    Component: React.ComponentType<P>
) {
    const displayName = Component.displayName || Component.name || 'Component';

    const wrapped = function (
        props: P & React.ComponentProps<typeof BasePage>
    ) {
        return (
            <BasePage {...props} _class={Component.name}>
                <Component {...props} />
            </BasePage>
        );
    };

    wrapped.displayName = `basePageWrap(${displayName})`;

    return wrapped;
}

export default BasePage;

