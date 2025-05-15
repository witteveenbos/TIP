import React from 'react';
import StartupDialog from './StartupDialog';
import data from './StartupDialog.data';

export default {
    title: 'Components/StartupDialog',
    component: StartupDialog,
};

export const StartupDialogWithoutData = () => <StartupDialog />;
export const StartupDialogWithData = () => <StartupDialog {...data} />;
