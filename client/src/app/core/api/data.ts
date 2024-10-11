import axios from 'axios';

//PAISES START//
export async function getAllPaises() {
    const url: string = `http://localhost:8888/api/core/paises/`;
    try {
        const response = await axios.get(url);
        console.log('response getAllPaises', response.data);
        return response.data;
    } catch (error: any ) {
        if(error.response.status === 400){
            throw error.response;
        } else {
            throw `Error en la solicitud: ${error.message}`;
        }
    }
}

export async function getOnePais(id: number) {
    const url: string = `http://localhost:8888/api/core/paises/${id}/`;
    try {
        const response = await axios.get(url);
        console.log('response getOnePais', response.data);
        return response.data;
    } catch (error: any ) {
        if(error.response.status === 400){
            throw error.response;
        } else {
            throw `Error en la solicitud: ${error.message}`;
        }
    }
}

//PAISES END//

//COMUNIDADES AUTONOMAS START//

export async function getAllComunidadesAutonomas() {
    const url: string = `http://localhost:8888/api/core/comunidades/`;
    try {
        const response = await axios.get(url);
        console.log('response getAllComunidadesAutonomas', response.data);
        return response.data;
    } catch (error: any ) {
        if(error.response.status === 400){
            throw error.response;
        } else {
            throw `Error en la solicitud: ${error.message}`;
        }
    }
}

export async function getOneComunidadesAutonomas(id: number) {
    const url: string = `http://localhost:8888/api/core/comunidades/${id}/`;
    try {
        const response = await axios.get(url);
        console.log('response getOneComunidadesAutonomas', response.data);
        return response.data;
    } catch (error: any ) {
        if(error.response.status === 400){
            throw error.response;
        } else {
            throw `Error en la solicitud: ${error.message}`;
        }
    }
}

//COMUNIDADES AUTONOMAS END//




//PROVINCIAS START//


export async function getAllProvincias() {
    const url: string = `http://localhost:8888/api/core/provincias/`;
    try {
        const response = await axios.get(url);
        console.log('response getAllProvincias', response.data);
        return response.data;
    } catch (error: any ) {
        if(error.response.status === 400){
            throw error.response;
        } else {
            throw `Error en la solicitud: ${error.message}`;
        }
    }
}

export async function getOneProvincias(id: number) {
    const url: string = `http://localhost:8888/api/core/provincias/${id}/`;
    try {
        const response = await axios.get(url);
        console.log('response getOneProvincias', response.data);
        return response.data;
    } catch (error: any ) {
        if(error.response.status === 400){
            throw error.response;
        } else {
            throw `Error en la solicitud: ${error.message}`;
        }
    }
}

//PROVINCIAS END//



export async function getProvinciasRegister(){
    const url: string = `http://127.0.0.1:8888/api/core/provincias/register/`;
    try {
        const response = await axios.get(url);
        console.log('response getProvinciasRegister', response.data);
        if(response.data.status === 'success'){ 
            console.log('response getProvinciasRegister', response.data);
            return response.data.data;
        }
    } catch (error: any ) {
        if(error.response.status === 400){
            throw error
        } else {
            throw `Error en la solicitud: ${error.message}`;
        }
    }
}