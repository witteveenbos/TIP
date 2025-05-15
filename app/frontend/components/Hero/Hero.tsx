import logo from '../../public/img/logo.svg';

import i18n from '../../i18n';

const Hero = ({ title }) => (
    <div>
        <img src={logo.src} width={logo.width} height={logo.height} />
        <h1>
            <img src={'/img/white_circle.png'} alt="Logo" />
            {title}
        </h1>
        <p>{i18n.t('helloWorld')}</p>
    </div>
);

export default Hero;
