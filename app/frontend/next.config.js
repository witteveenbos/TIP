const { transpile } = require('typescript');
const { i18n } = require('./next-i18next.config');

const basePath = '';

let nextConfig = {
    trailingSlash: true,
    productionBrowserSourceMaps: true,
    basePath,
    i18n,
    output: 'standalone',
    webpack: true,
    reactStrictMode: true,
    trailingSlash: true,
    productionBrowserSourceMaps: true,
    typescript: {
        // !! WARN !!
        // Dangerously allow production builds to successfully complete even if
        // your project has type errors.
        // !! WARN !!
        ignoreBuildErrors: true,
    },
    transpilePackages: [
        'radix-ui',
        'react-joyride',
        '@radix-ui/react-accessible-icon',
        '@radix-ui/react-accordion',
        '@radix-ui/react-alert-dialog',
        '@radix-ui/react-arrow',
        '@radix-ui/react-aspect-ratio',
        '@radix-ui/react-avatar',
        '@radix-ui/react-checkbox',
        '@radix-ui/react-collapsible',
        '@radix-ui/react-collection',
        '@radix-ui/react-context',
        '@radix-ui/react-context-menu',
        '@radix-ui/react-dialog',
        '@radix-ui/react-direction',
        '@radix-ui/react-dissmissable-layer',
        '@radix-ui/react-dropdown-menu',
        '@radix-ui/react-focus-scope',
        '@radix-ui/react-form',
        '@radix-ui/react-hover-card',
        '@radix-ui/react-label',
        '@radix-ui/react-menu',
        '@radix-ui/react-menubar',
        '@radix-ui/react-navigation-menu',
        '@radix-ui/react-one-time-password-field',
        '@radix-ui/react-password-toggle-field',
        '@radix-ui/react-popover',
        '@radix-ui/react-popper',
        '@radix-ui/react-portal',
        '@radix-ui/react-primitive',
        '@radix-ui/react-progress',
        '@radix-ui/react-radio-group',
        '@radix-ui/react-roving-focus',
        '@radix-ui/react-scroll-area',
        '@radix-ui/react-select',
        '@radix-ui/react-separator',
        '@radix-ui/react-slider',
        '@radix-ui/react-slot',
        '@radix-ui/react-switch',
        '@radix-ui/react-tabs',
        '@radix-ui/react-toast',
        '@radix-ui/react-toggle',
        '@radix-ui/react-toggle-group',
        '@radix-ui/react-toolbar',
        '@radix-ui/react-tooltip',
        '@radix-ui/react-visually-hidden',
        '@storybook/preset-react-webpack',
        'eslint-plugin-react',
    ],
    images: {
        domains: ['localhost', 'nginx-accept-app.niceflower-dd2b93bc.westeurope.azurecontainerapps.io', 'frontend-accept-app.niceflower-dd2b93bc.westeurope.azurecontainerapps.io'],
    },
    async rewrites() {
        return [
            {
                source: '/wt/static/:path*',
                destination: 'https://backend-accept-app.niceflower-dd2b93bc.westeurope.azurecontainerapps.io/wt/static/:path*', // Proxy to Backend
            },
            {
                source: '/wt/media/:path*',
                destination: 'https://backend-accept-app.niceflower-dd2b93bc.westeurope.azurecontainerapps.io/wt/media/:path*', // Proxy to Backend
            },
        ];
    },
};

module.exports = () => {
    const plugins = [];
    return plugins.reduce((acc, plugin) => plugin(acc), {
        ...nextConfig,
    });
};
