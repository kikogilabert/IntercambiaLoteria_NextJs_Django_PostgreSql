import axios from 'axios';
import {  RegisterUserFormData, userLoginType, UserProfileData} from '@core/interfaces/user.interface';
import { CustomStorage } from '../common/local-storage';
import { StorageVariables } from '../constants';

export async function registerUser(formData: RegisterUserFormData) {
    const url: string = `http://localhost:8888/usuario/register/`;
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
    const url: string = `http://localhost:8888/usuario/login/`;
    try {
        console.log('loginData: ', formData)

        const response = await axios.post(url, {
            "email": formData.email,
            "password": formData.contraseña
        });
        if(response.data.status === 'success' && response.data.data.access_token) {
            let token = response.data.data.access_token;
            CustomStorage.setItem(StorageVariables.UserToken, token);
            console.log('token: ', token);
           await getUserLoggedProfile(token).then(
                (res) => {
                    console.log('UserData: ', res);
                    CustomStorage.setItem(StorageVariables.UserData, res);
                }
            ).catch(
                (error) => {
                    console.log(error);
                    
                }
            )
         
            return response.data;
        }
        else  {
            console.log('error');
        }
    } catch (error: any ) {
        console.log('error: ', error);
        // if(error.response.status === 400){
        //     throw error.response;
        // } else {
        //     throw `Error en la solicitud: ${error.message}`;
        // }
    }
}


export async function getUserLoggedProfile(token: string): Promise<UserProfileData> {
    return new Promise(
        (resolve, reject) => {
            const url = 'http://localhost:8888/usuario/profile/'
            if (token !== null) {
                axios.get(url, { "headers": { "Authorization": `Bearer ${token}` } }).then(
                    res => {
                        if (res && "data" in res) {
                            console.log('respuesta de getUserLoggedProfile: ', res.data);
                            resolve(res.data)
                        } else {
                            reject(res)
                        }
                    },
                    error => {
                        reject(error)
                    }
                )
            } else {
                reject('could not get user profile, wrong token')
            }
        }
    )
}
