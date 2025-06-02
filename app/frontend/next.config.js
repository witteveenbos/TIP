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
        'react-joyride',
        '@radix-ui/react-checkbox',
        '@radix-ui/react-dialog',
        '@radix-ui/react-label',
        '@radix-ui/react-navigation-menu',
        '@radix-ui/react-popover',
        '@radix-ui/react-radio-group',
        '@radix-ui/react-scroll-area',
        '@radix-ui/react-select',
        '@radix-ui/react-slot',
        '@radix-ui/react-switch',
        '@radix-ui/react-tabs',
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
