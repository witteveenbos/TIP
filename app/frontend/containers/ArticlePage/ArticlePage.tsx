import PropTypes from 'prop-types';
import React from 'react';
import EnergyBalance from '../../components/EnergyBalance';
import Hero from '../../components/Hero';
import RawHtml from '../../components/RawHtml';
import { basePageWrap } from '../BasePage';

const ArticlePage = ({ title, richText }) => {
    return (
        <div>
            <EnergyBalance />
            <Hero title={title} />
            <RawHtml html={richText} />
        </div>
    );
};

ArticlePage.defaultProps = {
    title: '',
    richText: '',
};

ArticlePage.propTypes = {
    title: PropTypes.string.isRequired,
    richText: PropTypes.string,
};

export default basePageWrap(ArticlePage);
