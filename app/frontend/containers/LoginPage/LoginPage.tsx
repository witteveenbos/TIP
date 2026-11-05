import { getRequest, postRequest } from '@/api/requests';
import { LoginPageProps } from '@/types/containers/loginPage';
import { useSearchParams } from 'next/navigation';
import React, { useState } from 'react';
import s from './LoginPage.module.css';

const getSafeReturnUrl = (
    nextUrl: string | null,
    fallbackUrl: string | null
): string => {
    const candidateUrl = nextUrl || fallbackUrl;
    if (!candidateUrl) {
        return '/';
    }

    try {
        const url = new URL(candidateUrl, 'http://safe-localhost');
        if (
            url.origin !== 'http://safe-localhost' ||
            !candidateUrl.startsWith('/')
        ) {
            return '/';
        }

        return `${url.pathname}${url.search}${url.hash}`;
    } catch {
        return '/';
    }
};

const LoginPage = ({
    titleLabel,
    usernameLabel,
    passwordLabel,
    buttonLoginText,
    invalidLogin,
    redirectPageUrl,
    buttonLogoutText,
}: LoginPageProps) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState<string | null>(null);
    const searchParams = useSearchParams();
    const returnUrl = getSafeReturnUrl(
        searchParams?.get('next') || null,
        redirectPageUrl
    );

    const NEXT_PUBLIC_API_URL: string =
        process.env.NEXT_PUBLIC_WAGTAIL_API_URL || '';

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        try {
            await getRequest(`${NEXT_PUBLIC_API_URL}/v1/csrf/`);
            const response = await postRequest(
                `${NEXT_PUBLIC_API_URL}/v1/login/`,
                {
                    username,
                    password,
                }
            );

            if (response) {
                // Redirect to the return URL or home page after successful login
                window.location.href = returnUrl;
            }
        } catch (err) {
            setError(invalidLogin);
        }
    };

    return (
        <>
            <div className={s.loginpage}>
                {titleLabel && <h2>{titleLabel}</h2>}
                <form onSubmit={handleSubmit} className={s.loginpage__form}>
                    <div>
                        <label htmlFor="username">{usernameLabel}</label>
                        <input
                            id="username"
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                            placeholder={usernameLabel}
                            autoComplete="current-username"
                            className={s.loginpage__input}
                        />
                    </div>
                    <div>
                        <label htmlFor="password">{passwordLabel}</label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            placeholder={passwordLabel}
                            autoComplete="current-password"
                            className={s.loginpage__input}
                        />
                    </div>
                    {error && (
                        <div style={{ color: 'red', marginBottom: 16 }}>
                            {error}
                        </div>
                    )}
                    <button title={buttonLoginText}>{buttonLoginText}</button>
                </form>
            </div>
        </>
    );
};

export default LoginPage;
