import axios from 'axios';
import {  RegisterUserFormData, userLoginType, UserProfileData} from '@core/interfaces/user.interface';
import { CustomStorage } from '../common/local-storage';
import { StorageVariables } from '../constants';

export async function registerUser(formData: RegisterUserFormData) {
    const url: string = `http://localhost:8888/api/usuario/register/`;
    try {
        console.log('registerdata: ', formData)
        const response = await axios.post(url, {
            "usuario": {
                "tipo": formData.usuario.tipo,
                "dni": formData.usuario.dni,
                "nombre": formData.usuario.nombre,
                "apellidos": formData.usuario.apellidos,
                "password1": formData.usuario.password1,
                "password2": formData.usuario.password2,
                "telefono": formData.usuario.telefono,
                "email": formData.usuario.email
            },
            "administracion": {
                "nombre_comercial": formData.administracion.nombre_comercial,
                "numero_receptor": formData.administracion.numero_receptor,
                "direccion": formData.administracion.direccion,
                "provincia": formData.administracion.provincia,
                "localidad": formData.administracion.localidad,
                "codigo_postal": formData.administracion.codigo_postal,
                "numero_administracion": formData.administracion.numero_administracion
            }
        });
        return response.data;
    } catch (error: any ) {
        if(error.response.status === 400){
            throw error.response;
        } else {
            throw `Error en la solicitud: ${error.message}`;
        }
    }
}

export async function loginUser(formData: userLoginType) {
    const loginUrl: string = `http://localhost:8888/api/usuario/login/`;
    const profileUrl: string = `http://localhost:8888/api/usuario/profile/`;

    try {
        // Primera petición para obtener el token
        const loginResponse = await axios.post(loginUrl, {
            "email": formData.email,
            "password": formData.contraseña
        });

        if(loginResponse.data.status === 'success' && loginResponse.data.data.access_token) {
            let token = loginResponse.data.data.access_token;
            CustomStorage.setItem(StorageVariables.UserToken, token);

            // Segunda petición para obtener los datos del usuario
            const profileResponse = await axios.get(profileUrl, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            console.log('profileResponse', profileResponse.data);
                
            if(profileResponse !== null) {
                let userData = profileResponse.data;
                CustomStorage.setItem(StorageVariables.UserData, userData);
                return userData;
            } else {
                throw new Error('Failed to fetch user profile');
            }
        } else {
            throw new Error('Something went wrong at login');
        }
    } catch (error: any ) {
        console.error(error);
        throw error.response.data;
    }
}

export async function updateUserData(userData: UserProfileData, token: string) {
    const url: string = `http://localhost:8888/api/usuario/profile/update/`;
    console.log('userData dentro de la funcion', userData);
    
    try {
        const response = await axios.patch(url, userData, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        console.log('response updateUserData', response.data);
        return response.data;
    } catch (error: any ) {
        if(error.response.status === 400){
            throw error.response;
        } else {
            throw `Error en la solicitud: ${error.message}`;
        }
    }
}