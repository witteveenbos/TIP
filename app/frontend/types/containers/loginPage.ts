export interface LoginPageProps {
    titleLabel?: string | null;
    usernameLabel: string;
    passwordLabel: string;
    buttonLoginText: string;
    invalidLogin: string;
    redirectPageUrl: string | null;
    buttonLogoutText: string;
}
