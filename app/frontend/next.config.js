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
    transpilePackages: ['radix-ui'],
    images: {
        domains: ['localhost'],
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
