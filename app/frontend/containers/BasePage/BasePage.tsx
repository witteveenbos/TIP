import Header from '@/components/Header';
import dynamic from 'next/dynamic';
import Head from 'next/head';
import React from 'react';

const WagtailUserbar = dynamic(() => import('../../components/WagtailUserbar'));

interface SeoProps {
    seoHtmlTitle?: string;
    seoMetaDescription?: string;
    seoOgTitle?: string;
    seoOgDescription?: string;
    seoOgUrl?: string;
    seoOgImage?: string;
    seoOgType?: string;
    seoTwitterTitle?: string;
    seoTwitterDescription?: string;
    seoTwitterUrl?: string;
    seoTwitterImage?: string;
    canonicalLink?: string;
    seoMetaRobots?: string;
}

interface WagtailUserbarProps {
    html?: string;
}

interface NavItemProps {
    title: string;
    slug: string;
    submenu: Array<any>;
}

interface BasePageProps {
    children?: React.ReactNode;
    seo: SeoProps;
    wagtailUserbar?: WagtailUserbarProps;
    siteSetting?: {
        logo: {
            url: string;
        };
        favicon: {
            url: string;
        };
    };
    navigation?: Array<NavItemProps>;
}

const BasePage = ({
    children,
    seo,
    wagtailUserbar,
    siteSetting,
    navigation,
}: BasePageProps) => {
    const {
        seoHtmlTitle,
        seoMetaDescription,
        seoOgTitle,
        seoOgDescription,
        seoOgUrl,
        seoOgImage,
        seoOgType,
        seoTwitterTitle,
        seoTwitterDescription,
        seoTwitterUrl,
        seoTwitterImage,
        seoMetaRobots,
        canonicalLink,
    } = seo;
    const { logo, favicon } = siteSetting;

    return (
        <>
            <Head>
                <title>{seoHtmlTitle}</title>

                <link
                    rel="icon"
                    href={favicon ? favicon.url : '/favicon.ico'}
                />

                {!!seoMetaDescription && (
                    <meta name="description" content={seoMetaDescription} />
                )}
                {!!seoOgTitle && (
                    <meta property="og:title" content={seoOgTitle} />
                )}
                {!!seoOgDescription && (
                    <meta
                        property="og:description"
                        content={seoOgDescription}
                    />
                )}
                {!!seoOgUrl && <meta property="og:url" content={seoOgUrl} />}
                {!!seoOgImage && (
                    <meta property="og:image" content={seoOgImage} />
                )}
                {!!seoOgType && <meta property="og:type" content={seoOgType} />}
                {!!seoTwitterTitle && (
                    <meta property="twitter:title" content={seoTwitterTitle} />
                )}
                {!!seoTwitterDescription && (
                    <meta
                        property="twitter:description"
                        content={seoTwitterDescription}
                    />
                )}
                {!!seoTwitterUrl && (
                    <meta property="twitter:url" content={seoTwitterUrl} />
                )}
                {!!seoTwitterImage && (
                    <meta property="twitter:image" content={seoTwitterImage} />
                )}
                <meta name="robots" content={seoMetaRobots} />
                {!!canonicalLink && (
                    <link rel="canonical" href={canonicalLink} />
                )}
            </Head>
            <div className="flex flex-col h-full">
                <Header logo={logo}></Header>

                <div className="flex-1 relative" id="map">
                    {children}
                </div>
            </div>
            {!!wagtailUserbar && <WagtailUserbar {...wagtailUserbar} />}
        </>
    );
};

export default BasePage;
