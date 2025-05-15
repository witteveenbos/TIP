/* global module */

import React from 'react';
import EnergyBalance from './EnergyBalance';

import data from './EnergyBalance.data';

export default {
    title: 'Components/EnergyBalance',
    component: EnergyBalance,
};

export const EnergyBalanceWithoutData = () => <EnergyBalance />;
export const EnergyBalanceWithData = () => <EnergyBalance {...data} />;
