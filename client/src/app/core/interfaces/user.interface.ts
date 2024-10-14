export enum UsuarioTypeEnum {
    PF = 'PF', //PERSONA FISICA
    PJ = 'PJ' //PERSONA JURIDICA
}

export type userRegisterType = {
    tipo: string;
    dni: string;
    nombre: string;
    apellidos: string;
    password1: string;
    password2: string;
    telefono: string;
    email: string;
    ServerError?: any;

}

export type administracionRegisterType = {
    nombre_comercial: string;
    numero_receptor: string;
    direccion: string;
    provincia: string;
    localidad: string;
    codigo_postal: string;
    numero_administracion: string;
    ServerError?: any;
}

export type RegisterUserFormData = {
usuario: userRegisterType;
administracion: administracionRegisterType;
}

export type userLoginType = {
    email: string;
    contraseña: string;
    ServerError?: any;
}

export type userLoginResponse = {
    state: string;  
    error_code?: string;
    access_token: string;
    refresh_token: string;
}


export interface UserProfileData {
    tipo: UsuarioTypeEnum;
    nombre: string;
    apellidos: string;
    email: string;
    telefono: string;
    dni: string;
    administracion: Number;
}


export interface AdministracionProfileData {
    nombre_comercial: string;
    numero_receptor: string;
    direccion: string;
    localidad: string;
    codigo_postal: string;
    provincia: string;
    numero_administracion: string;
}