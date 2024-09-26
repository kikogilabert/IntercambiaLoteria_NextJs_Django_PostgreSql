"use client"

import { Button, Input, Select, SelectItem, SelectSection } from '@nextui-org/react';
import { useState } from 'react';
import { PROVINCIAS_POR_COMUNIDAD, TIPO_PROPIETARIO } from '@core/constants/index';
import { UsuarioInterface, AdministracionInterface } from '@core/interfaces/user.interface';
import './register_form.module.scss'

import { useForm } from "react-hook-form";
import { z } from 'zod';
import { zodResolver } from "@hookform/resolvers/zod";


type ProvinciaType = {
    name: string;
    value: string;
}

export default function RegisterComponent() {
    ////////////////////schemas/////////////////////////
    const userSchema = z.object({
        tipo: z.string().refine(value => ['PF', 'PJ'].includes(value), {
            message: 'Tipo debe ser "Persona Fisica" o "Persona Juridica"',
        }),
        dni: z.string().length(9, { message: 'DNI debe tener 9 caracteres' }),
        nombre: z.string({ message: 'Nombre es requerido' }).min(5, { message: 'Nombre debe tener al menos 5 caracteres' }).max(30, { message: 'Nombre debe tener menos de 30 caracteres' }),
        apellidos: z.string().nullable(),
        password: z.string({ message: 'Contraseña es requerida' }).min(8, { message: 'Contraseña debe tener al menos 8 caracteres' }).max(30, { message: 'Contraseña debe tener menos de 30 caracteres' }),
        confirm_password: z.string({ message: 'Confirmar contraseña es requerida' }).min(8, { message: 'Confirmar contraseña debe tener al menos 8 caracteres' }).max(30, { message: 'Confirmar contraseña debe tener menos de 30 caracteres' }),
        phoneNumber: z.string({ message: 'Número de teléfono es requerido' }).length(9, { message: 'Número de teléfono debe tener 9 caracteres' }),
        email: z.string().email({ message: 'Email no es válido' }).nonempty({ message: 'Email es requerido' }),
    });

    const adminSchema = z.object({
        nombreComercial: z.string({ message: 'Nombre de administrador es requerido' }).min(5, { message: 'Nombre de administrador debe tener al menos 5 caracteres' }).max(30, { message: 'Nombre de administrador debe tener menos de 30 caracteres' }),
        numeroReceptor: z.string().length(5, { message: 'Número receptor debe tener 5 caracteres' }),
        direccion: z.string({ message: 'Dirección es requerida' }).min(5, { message: 'Dirección debe tener al menos 5 caracteres' }).max(30, { message: 'Dirección debe tener menos de 30 caracteres' }),
        provincia: z.string({ message: 'Provincia es requerida' }).min(5, { message: 'Provincia debe tener al menos 5 caracteres' }).max(30, { message: 'Provincia debe tener menos de 30 caracteres' }),
        localidad: z.string({ message: 'Localidad es requerida' }).min(5, { message: 'Localidad debe tener al menos 5 caracteres' }).max(30, { message: 'Localidad debe tener menos de 30 caracteres' }),
        numeroAdministracion: z.number().min(0, { message: 'Número de administración debe ser mayor a 0' }).max(2000, { message: 'Número de administración debe ser menor a 2000' }),
    });



    //////////////////////////////// VARIABLES////////////////////////////////

    const [usuario, setUsuario] = useState<UsuarioInterface | null>();
    const [administracion, setAdministracion] = useState<AdministracionInterface | null>(null);
    const [step, setStep] = useState(0);
    const [isButtonLoading, setIsButtonLoading] = useState(false)


    //////////////////////////////// FUNCTIONS////////////////////////////////
    const { register, handleSubmit,
        setValue,
        setError,
        formState: { errors } } =
        useForm({
            resolver: zodResolver(step === 0 ? adminSchema : userSchema),
            mode: 'onChange',
            defaultValues: step === 0 ? { nombre_comercial: '', numero_receptor: '', direccion: '', provincia: '', localidad: '', numero_administracion: '' } :  { tipo: '', dni: '', nombre: '', apellidos: '', contraseña: '', confirmar_contraseña: '', telefono: '', email: '' } 
        });
        console.log(errors);
        
    //submit form function
    const onSubmit = (data: any) => {
        if (step === 0) {
            setAdministracion(data);
            setStep(1);
            setIsButtonLoading(false);
        } else {
            setUsuario(data);
            const finalData = { usuario: usuario, administracion: administracion };
            setIsButtonLoading(false);

            console.log(finalData);
        }
    };


    return (

        <div className='w-full flex justify-center items-center'>
            {
                step == 0 &&
                <form className='flex flex-col w-full justify-center items-center gap-6 h-full max-w-[765px]' onSubmit={handleSubmit(data => onSubmit(data))}>
                    <h2 className='text-2xl font-bold'>Cuentanos sobre tu administracion...</h2>
                    <div className='flex flex-col gap-4 items-center justify-center max-w-[365px] w-full h-full'>
                        <Input
                        {...register('nombre_comercial')}
                        onChange={(e) => setValue('nombre_comercial', e.target.value)}
                            isRequired type="text"
                            label="Nombre Comercial" placeholder=''
                            size='sm'
                        />
                        <Input
                            {...register('numero_receptor')}
                            onChange={(e) => setValue('numero_receptor', e.target.value)}
                            isRequired type="number"
                            label="Número receptor"
                            maxLength={5}
                            minLength={5} placeholder='' size='sm'
                        />
                        <Input 
                            {...register('direccion')}
                            onChange={(e) => setValue('direccion', e.target.value)}
                            isRequired type="text"
                            label="Dirección" placeholder=''
                            size='sm' 
                        />
                        <Select
                            {...register('provincia')}
                            onChange={(e) => setValue('provincia', e.target.value)}
                            isRequired
                            label="Provincia"
                            placeholder="Selecciona una provincia"
                            size='sm'
                            scrollShadowProps={{
                                isEnabled: false
                            }}
                        >
                            {PROVINCIAS_POR_COMUNIDAD.map((comunidad) => (
                            <SelectSection title={comunidad.comunidad} key={comunidad.comunidad}>
                                {comunidad.provincias.map((provincia) => (
                                <SelectItem key={provincia.value}>
                                    {provincia.name}
                                </SelectItem>
                                ))}
                            </SelectSection>
                            ))}
                        </Select>
                        <Input 
                            {...register('localidad')} 
                            onChange={(e) => setValue('localidad', e.target.value)}
                            isRequired type="text"
                            label="Localidad" placeholder=''
                            size='sm'
                        />
                        <Input 
                            {...register('numero_administracion')}
                            onChange={(e) => setValue('numero_administracion', e.target.value)}
                            isRequired type="number" 
                            label="Número Administración" min={0} 
                            max={5000} placeholder='' size='sm' 
                        />
                    </div>
                    <div className='flex flex-row gap-[8px] justify-center items-center w-full'>
                        <Button className='flex w-full max-w-xs' type='submit' color="primary" variant="ghost" isLoading={isButtonLoading}>
                            Continuar
                        </Button>
                    </div>
                </form>
            }
            {
                step === 1 &&
                <form className='flex flex-col w-full justify-center items-center gap-10 h-full max-w-[765px]' onSubmit={handleSubmit(data => onSubmit(data))}>
                    <h2 className='text-2xl font-bold'>Y quien es el valiente a cargo de ella...</h2>
                    <div className='flex flex-col gap-4 items-center justify-center w-full max-w-[365px] h-full'>
                        <Select
                            {...register('tipo')}
                            onChange={(e) => setValue('tipo', e.target.value)}

                            isRequired size='sm'
                            label="Tipo de Propietario"
                            placeholder=''
                            scrollShadowProps={{
                                isEnabled: false
                            }}
                        >
                            {TIPO_PROPIETARIO.map((tipo) => (
                                <SelectItem key={tipo.value}>
                                    {tipo.name}
                                </SelectItem>
                            ))}
                        </Select>
                        <Input isRequired size='sm' type="text" label="DNI" placeholder='' />
                        <div className='flex flex-row gap-[8px] max-w-full'>
                            <Input {...register('nombre')} onChange={(e) => setValue('nombre', e.target.value)} isRequired size='sm' type="text" label="Nombre" placeholder='' />
                            <Input isRequired size='sm'  {...register('apellidos')}  onChange={(e) => setValue('apellidos', e.target.value)} type="text" label="Apellidos" placeholder='' />
                        </div>
                        <Input isRequired size='sm' type="tel" label="Telefono" {...register('telefono')}  onChange={(e) => setValue('telefono', e.target.value)} placeholder='' />
                        <Input isRequired size='sm' type="email" label="Email" placeholder='' {...register('email')}  onChange={(e) => setValue('email', e.target.value)} />
                        <Input isRequired size='sm' type="text" label="Contraseña" placeholder=''  {...register('contraseña')}  onChange={(e) => setValue('contraseña', e.target.value)} />
                        <Input isRequired size='sm' type="text" label="Confirma contraseña" placeholder=''  {...register('confirmar_contraseña')}  onChange={(e) => setValue('confirmar_contraseña', e.target.value)} />
                    </div>
                    <div className='flex'>
                        <Button className='flex w-full max-w-xs' type='submit' color="primary" variant="ghost" isLoading={isButtonLoading}>
                            Registrarse
                        </Button>
                    </div>
                </form>
            }

        </div>
    );
}