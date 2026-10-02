const { transpile } = require('typescript');
const { i18n } = require('./next-i18next.config');

const basePath = '';
const backendApiBase =
    process.env.WAGTAIL_API_URL ||
    'https://backend-accept-app.yellowsea-a6617e80.westeurope.azurecontainerapps.io/wt/api/nextjs';
const wagtailApiBase = new URL(
    process.env.NEXT_PUBLIC_WAGTAIL_API_URL || '/wt/api/nextjs',
    backendApiBase
)
    .toString()
    .replace(/\/$/, '');
const apiBase = new URL(
    process.env.NEXT_PUBLIC_API_URL || '/api',
    backendApiBase
)
    .toString()
    .replace(/\/$/, '');

let nextConfig = {
    trailingSlash: true,
    productionBrowserSourceMaps: true,
    basePath,
    i18n,
    output: 'standalone',
    webpack: true,
    turbopack: {},
    reactStrictMode: true,
    typescript: {
        // !! WARN !!
        // Dangerously allow production builds to successfully complete even if
        // your project has type errors.
        // !! WARN !!
        ignoreBuildErrors: true,
    },
    transpilePackages: [
        'react-joyride',
        '@radix-ui/react-slot',
        '@radix-ui/react-checkbox',
        '@radix-ui/react-context',
        '@radix-ui/react-dialog',
        '@radix-ui/react-label',
        '@radix-ui/react-navigation-menu',
        '@radix-ui/react-popover',
        '@radix-ui/react-radio-group',
        '@radix-ui/react-scroll-area',
        '@radix-ui/react-select',
        '@radix-ui/react-switch',
        '@radix-ui/react-tabs',
    ],
    images: {
        remotePatterns: [
            {
                protocol: 'http',
                hostname: 'localhost',
                pathname: '**',
            },
            {
                protocol: 'https',
                hostname: '*.azurecontainerapps.io',
                pathname: '**',
            },
        ],
    },
    async rewrites() {
        return [
            {
                source: '/wt/api/nextjs/:path*/',
                destination: `${wagtailApiBase}/:path*/`,
            },
            {
                source: '/api/:path*/',
                destination: `${apiBase}/:path*/`,
            },
            {
                source: '/wt/static/:path*',
                destination: 'https://backend-accept-app.yellowsea-a6617e80.westeurope.azurecontainerapps.io/wt/static/:path*', // Proxy to Backend
            },
            {
                source: '/wt/media/:path*',
                destination: 'https://backend-accept-app.yellowsea-a6617e80.westeurope.azurecontainerapps.io/wt/media/:path*', // Proxy to Backend
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
