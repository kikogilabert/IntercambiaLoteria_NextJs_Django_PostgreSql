"use client"

import { Button, Input, Select, SelectItem, SelectSection } from '@nextui-org/react';
import { Eye, EyeOff } from 'lucide-react';

import { Autocomplete, AutocompleteItem, AutocompleteSection } from "@nextui-org/react";
import { useState } from 'react';
import { PROVINCIAS_POR_COMUNIDAD, TIPO_PROPIETARIO } from '@core/constants/index';

import './register_form.module.scss'

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { registerUser } from '@/core/api/auth';
import { RegisterUserFormData, userRegisterType, administracionRegisterType } from '@core/interfaces/user.interface';
import { adminSchema, userSchema } from '@core/components/register/registerSchema';
import { useRouter } from 'next/navigation';

type registerComponentProps = {
    lista_comunidades: registerComunidades[]

}
type registerProvincias = {
    id: number,
    nombre: string
}
type registerComunidades = {
    nombre: string,
    provincias: registerProvincias[]
}

export default function RegisterComponent(props: registerComponentProps) {

    console.log(props.lista_comunidades);
    //////////////////////////////// VARIABLES////////////////////////////////
    const router = useRouter();
    const [usuario, setUsuario] = useState<userRegisterType | null>();
    const [administracion, setAdministracion] = useState<administracionRegisterType | null>(null);

    const [step, setStep] = useState(0);
    const [showPassword, setShowPassword] = useState(false);
    const [showPassword2, setShowPassword2] = useState(false);
    const [isButtonLoading, setIsButtonLoading] = useState(false)


    //////////////////////////////// FUNCTIONS////////////////////////////////
    const { register, handleSubmit,
        setValue,
        getValues,
        setError,
        formState: { errors } } =
        useForm({
            resolver: zodResolver(step === 0 ? adminSchema : userSchema),
            mode: 'onSubmit',
            defaultValues: step === 0 ? { nombre_comercial: '', numero_receptor: '', direccion: '', provincia: 0, localidad: '', codigo_postal: '', numero_administracion: '' }
                : { tipo: '', dni: '', nombre: '', apellidos: '', password1: '', password2: '', telefono: '', email: '' }
        });
    console.log(errors);

    //submit form function
    const onSubmit = (data: any) => {
        setIsButtonLoading(true);        
        if (step === 0) {
            data.provincia = selectedProvinciaID;
            console.log('administracion', data);
            setAdministracion(data);
            setStep(1);
            setIsButtonLoading(false);
        } if (step === 1) {
            setUsuario(data);
            setIsButtonLoading(false);
        }
        if (usuario && administracion) {
            const finalData: RegisterUserFormData = { usuario: usuario, administracion: administracion };
            console.log(finalData);
            const response = registerUser(finalData)
                .then((res) => {
                    console.log(res);
                    router.push('/iniciar-sesion');
                }
                ).catch((err) => {
                    console.log(err);
                    if (err.response.status === 400) {
                        setError('email', { message: 'Email ya registrado' });
                    }
                })
        }
    };

    const [selectedProvinciaID, setSelectedProvinciaID] = useState(""); // El valor seleccionado (ID de la provincia)

    // Controlar la selección del usuario
    const onSelectionChange = (key: any) => {
        console.log('key', key);
        setSelectedProvinciaID(key); // Actualiza el valor seleccionado (ID de la provincia)
      setValue('provincia', key); // Almacena el ID de la provincia en react-hook-form
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
                            isInvalid={errors.nombre_comercial ? true : false}
                            errorMessage={errors.nombre_comercial?.message ? errors.nombre_comercial?.message : null}
                            type="text"
                            label="Nombre Comercial" placeholder=''
                            size='sm'
                        />
                        <Input
                            {...register('numero_receptor')}
                            onChange={(e) => setValue('numero_receptor', e.target.value)}
                            isInvalid={errors.numero_receptor ? true : false}
                            errorMessage={errors.numero_receptor?.message ? errors.numero_receptor?.message : null}
                            isRequired type="number"
                            label="Número receptor"
                            maxLength={5}
                            placeholder='' size='sm'
                        />
                        <Input
                            {...register('direccion')}
                            onChange={(e) => setValue('direccion', e.target.value)}
                            isRequired type="text"
                            label="Dirección" placeholder=''
                            size='sm'
                            isInvalid={errors.direccion ? true : false}
                            errorMessage={errors.direccion?.message ? errors.direccion?.message : null}
                        />

                        <Autocomplete
                            {...register('provincia')}
                            selectedKey={selectedProvinciaID}
                            onSelectionChange={onSelectionChange} 
                            isInvalid={!!errors.provincia} 
                            errorMessage={errors.provincia?.message || null}
                            label="Provincia"
                            placeholder="Selecciona una provincia"
                            size='sm'
                            isRequired
                            scrollShadowProps={{ isEnabled: false }}
                        >
                            {props.lista_comunidades.map((comunidad, index) => (
                                <AutocompleteSection
                                    title={comunidad.nombre}
                                    key={comunidad.nombre}
                                    showDivider={index + 1 === props.lista_comunidades.length ? false : true}
                                >
                                    {comunidad.provincias.map((provincia) => (
                                        <AutocompleteItem key={provincia.id} value={provincia.id} textValue={provincia.nombre}>
                                            {provincia.nombre}
                                        </AutocompleteItem>
                                    ))}
                                </AutocompleteSection>
                            ))}
                        </Autocomplete>
                        <Input
                            {...register('localidad')}
                            onChange={(e) => setValue('localidad', e.target.value)}
                            isInvalid={errors.localidad ? true : false}
                            errorMessage={errors.localidad?.message ? errors.localidad?.message : null}
                            isRequired type="text"
                            label="Localidad" placeholder=''
                            size='sm'
                        />
                        <Input
                            {...register('codigo_postal')}
                            onChange={(e) => setValue('codigo_postal', e.target.value)}
                            isInvalid={errors.codigo_postal ? true : false}
                            errorMessage={errors.codigo_postal?.message ? errors.codigo_postal?.message : null}
                            isRequired type="text"
                            label="Codigo postal" placeholder=''
                            size='sm'
                        />
                        <Input
                            {...register('numero_administracion')}
                            onChange={(e) => setValue('numero_administracion', e.target.value)}
                            isInvalid={errors.numero_administracion ? true : false}
                            errorMessage={errors.numero_administracion?.message ? errors.numero_administracion?.message : null}
                            isRequired type="number"
                            label="Número Administración" placeholder='' size='sm'
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
                            isInvalid={errors.tipo ? true : false}
                            errorMessage={errors.tipo?.message ? errors.tipo?.message : null}
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
                        <Input
                            {...register('dni')}
                            onChange={(e) => setValue('dni', e.target.value)}
                            isInvalid={errors.dni ? true : false}
                            errorMessage={errors.dni?.message ? errors.dni?.message : null}
                            isRequired size='sm'
                            type="text" label="DNI/NIF/NIE"
                            placeholder=''
                        />
                        <div className='flex flex-row gap-[8px] max-w-full'>
                            <Input
                                {...register('nombre')}
                                onChange={(e) => setValue('nombre', e.target.value)}
                                isInvalid={errors.nombre ? true : false}
                                errorMessage={errors.nombre?.message ? errors.nombre?.message : null}
                                isRequired size='sm' type="text"
                                label="Nombre" placeholder=''
                            />
                            <Input
                                isRequired={getValues('tipo') === 'Persona Fisica' ? true : false} size='sm'
                                {...register('apellidos')}
                                onChange={(e) => setValue('apellidos', e.target.value)}
                                isInvalid={errors.apellidos ? true : false}
                                errorMessage={errors.apellidos?.message ? errors.apellidos?.message : null}
                                type="text" label="Apellidos"
                                placeholder=''
                            />
                        </div>
                        <Input
                            isRequired size='sm' type="tel"
                            label="Telefono" {...register('telefono')}
                            onChange={(e) => setValue('telefono', e.target.value)}
                            isInvalid={errors.telefono ? true : false}
                            errorMessage={errors.telefono?.message ? errors.telefono?.message : null}
                            placeholder=''
                        />
                        <Input
                            isRequired size='sm' type="email"
                            label="Email" placeholder='' {...register('email')}
                            onChange={(e) => setValue('email', e.target.value)}
                            isInvalid={errors.email ? true : false}
                            errorMessage={errors.email?.message ? errors.email?.message : null}
                        />
                        <Input
                            isRequired size='sm' type={showPassword ? 'text' : 'password'}
                            label="Contraseña" placeholder=''  {...register('password1')}
                            onChange={(e) => setValue('password1', e.target.value)}
                            isInvalid={errors.password1 ? true : false}
                            errorMessage={errors.password1?.message ? errors.password1?.message : null}
                            endContent={
                                showPassword ?
                                    <EyeOff onClick={() => setShowPassword(false)} className="cursor-pointer" /> :
                                    <Eye onClick={() => setShowPassword(true)} className="cursor-pointer" />
                            }
                        />
                        <Input
                            isRequired size='sm' type={showPassword2 ? 'text' : 'password'}
                            label="Confirmar contraseña" placeholder=''
                            {...register('password2')}
                            onChange={(e) => setValue('password2', e.target.value)}
                            isInvalid={errors.password2 ? true : false}
                            errorMessage={errors.password2?.message ? errors.password2?.message : null}
                            endContent={
                                showPassword2 ?
                                    <EyeOff onClick={() => setShowPassword2(false)} className="cursor-pointer" /> :
                                    <Eye onClick={() => setShowPassword2(true)} className="cursor-pointer" />
                            }
                        />
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