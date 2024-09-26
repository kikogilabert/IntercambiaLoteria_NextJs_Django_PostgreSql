export enum UsuarioTypeEnum {
    PF = 'PF', //PERSONA FISICA
    PJ = 'PJ' //PERSONA JURIDICA
}


export interface UsuarioInterface {
    tipo: UsuarioTypeEnum;
    dni: string;
    nombre: string;
    apellidos: string;
    telefono: string;
    email: string;
    id_administracion: number;
    password: string;
    confirm_password: string;
    ServerError?: any;
}

export interface AdministracionInterface{

    nombre_comercial: string;
    numero_receptor: string;
    direccion: string;
    provincia: string;
    localidad: string;
    numero_administracion: string;
    ServerError?: any;
}