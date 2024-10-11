"use client";

import { useContext, createContext, useState, useEffect, ReactNode } from "react";
import { UserProfileData } from "@core/interfaces/user.interface";
import { StorageVariables } from "../constants";
import { CustomStorage } from "../common/local-storage";

interface AuthProviderProps {
    children: ReactNode;
}


// Nuevo context para Auth
// const auth = useAuth();

// auth.user // es el objeto UserData guardado en storage, null si está vacio
// auth.token // es el token jwt, null si está vacío
// auth.login(user) // método para hacer login pasándole el objeto UserData, después de guardar token jwt ya que comprueba si está expirado o no
// auth.logout() // método para poner a null auth.user y auth.token así como borrar las variables del localstorage.

// Para saber si está logueado, solo poner [auth.user] en las dependencias del useEffect, ya que si cambia auth.user, ya comprueba si el token es válido o no
// Se puede utilizar en cualquier componente, ya que está añadido en el root layout

const AuthContext = createContext({
    user: null as UserProfileData | null,
    token: null as string | null,
    logOut: () => {},
    setLogin: (user: UserProfileData) => { }
});

const AuthProvider = ({ children }: AuthProviderProps) => {
    const [user, setUser] = useState<UserProfileData | null>(CustomStorage.getItem(StorageVariables.UserData) as UserProfileData | null);
    const [token, setToken] = useState<string | null>(CustomStorage.getItem(StorageVariables.UserToken) as string | null );

    useEffect(() => {
        const jwt: string | null = CustomStorage.getItem(StorageVariables.UserToken);
        if (user && jwt) {
            const expired = isTokenExpired(jwt);
            if (!expired) {
                setToken(jwt);
            } 
            else {
                logOut();
            }
        }
    }, [user]);

    const logOut = () => {
        setUser(null);
        setToken(null);
        CustomStorage.removeItem(StorageVariables.UserData);
        CustomStorage.removeItem(StorageVariables.UserToken);
    };

    const setLogin = (user: UserProfileData) => {
        setUser(user);
    }

    return (
        <AuthContext.Provider value={{ user, token, logOut, setLogin }}>
            {children}
        </AuthContext.Provider>
    );

};

export default AuthProvider;

export const useAuth = () => {
    return useContext(AuthContext);
};

function isTokenExpired(token: string | null): boolean {
    if (!token) return true;
    try {
        const arrayToken = token.split(".");
        const tokenPayload = JSON.parse(atob(arrayToken[1]));
        const currentTime = Math.floor(Date.now() / 1000);

        return currentTime > tokenPayload.exp;
    } catch (error) {
        console.error('Invalid JWT token', error);
        return true;
    }
}