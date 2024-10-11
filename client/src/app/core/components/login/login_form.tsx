"use client"
import { Button, Input } from '@nextui-org/react';
import { useForm } from 'react-hook-form';
import { useState }  from 'react';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Eye, EyeOff, Icon, CircleX } from 'lucide-react';
import { loginUser } from '@/core/api/auth';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/core/context/auth.context';

export default function LoginForm() {
    const router = useRouter();
    const auth = useAuth();
    const [isButtonLoading, setIsButtonLoading] = useState(false)
    const [showPassword, setShowPassword] = useState(false)
    const onSubmit = async (data: any) => {
        setIsButtonLoading(true);
        console.log('before sendind', data);
        await loginUser(data).then(
          async (response) => {
                // console.log(response);
                auth.setLogin(response);
                setIsButtonLoading(false);
                router.push('/');
            }
        ).catch((error) => {
            console.log(error);
            setIsButtonLoading(false);
            if(error.status === 'error'){
                setError('ServerErrors', {
                    type: 'manual',
                    message: error.message
                })
            }
            // setError('ServerErrors', {
            //     type: 'manual',
            //     message: error.data.message
            // })
        })
    } 

    const loginSchema = z.object({
        email: z.string().email({ message: 'Email no es válido' }),
        contraseña: z.string().min(8, { message: 'Contraseña debe tener al menos 8 caracteres' }).max(30, { message: 'Contraseña debe tener menos de 30 caracteres' })
    })


    const { register, handleSubmit,
        setValue,
        getValues,
        setError,
        formState: { errors } } =
        useForm({
            resolver: zodResolver(loginSchema),
            mode: 'onSubmit',
            defaultValues: { email: '', contraseña: '', ServerErrors: '' }

        });
    console.log(errors);

    return (
        <div className='w-full flex justify-center items-center w-full h-full min-h-[90vh] '>
            <form className='flex flex-col w-full justify-center items-center gap-6 h-full max-w-[765px]' onSubmit={handleSubmit(data => onSubmit(data))}>
                <h2 className='text-2xl font-bold'>Inicia Sesión</h2>
                <div className='flex flex-col gap-4 items-center justify-center max-w-[365px] w-full h-full'>
                    <Input
                        isRequired
                        {...register('email')}
                        onChange={(e) => setValue('email', e.target.value)}
                        isInvalid={errors.email ? true : false}
                        errorMessage={errors.email?.message ? errors.email?.message : null}
                        type="text"
                        label="Email" placeholder=''
                        size='sm'
                    />
                    <Input
                        {...register('contraseña')}
                        onChange={(e) => setValue('contraseña', e.target.value)}
                        isInvalid={errors.contraseña ? true : false}
                        errorMessage={errors.contraseña?.message ? errors.contraseña?.message : null}
                        isRequired type={showPassword ? 'text' : 'password'}
                        endContent={ 
                            showPassword ? 
                            <EyeOff onClick={() => setShowPassword(false)} className="cursor-pointer" /> : 
                            <Eye onClick={() => setShowPassword(true)} className="cursor-pointer" />
                        }
                        label="Contraseña"
                        placeholder='' size='sm'
                    />
                    {/* <div className='flex flex-row justify-end items-center w-full'>
                        <Button color='primary'>¿Olvidaste tu contraseña?</Button>
                    </div> */}
                </div>
                {errors.ServerErrors && 
                <div className=' max-w-[365px] w-full items-center px-3 py-1 bg-[#FF9494] rounded flex flex-row gap-[8px]'>
                    <CircleX strokeWidth={1.25} size={'20px'} absoluteStrokeWidth  />
                    <p className='bold text-md'>{errors.ServerErrors.message}</p>
                </div> }
                <div className='flex flex-row gap-[8px] justify-center items-center w-full'>
                    <Button className='flex w-full max-w-xs' type='submit' color="primary" variant="ghost" isLoading={isButtonLoading}>
                        Continuar
                    </Button>
                </div>
            </form>
        </div>
    )



}