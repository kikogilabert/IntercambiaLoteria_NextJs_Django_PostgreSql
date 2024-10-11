import { z } from 'zod';
   ////////////////////schemas/////////////////////////
export  const adminSchema = z.object({
        nombre_comercial: z.string().min(5, { message: 'Nombre comercial debe tener al menos 5 caracteres' }).max(50, { message: 'Nombre comercial debe tener menos de 50 caracteres' }).nullable(),
        numero_receptor: z.string({ message: 'El numero de receptor es requerido' }).length(5, { message: 'Número receptor debe tener 5 caracteres' }),
        direccion: z.string({ message: 'Dirección es requerida' }).min(5, { message: 'Dirección debe tener al menos 5 caracteres' }).max(50, { message: 'Dirección debe tener menos de 50 caracteres' }),
        provincia: z.string({ message: 'Provincia es requerida' }),
        localidad: z.string({ message: 'Localidad es requerida' }),
        codigo_postal: z.string().length(5, { message: 'Código postal debe tener 5 caracteres' }),
        numero_administracion: z.string().min(1, { message: 'Número administracion es requerido.' }).max(3, { message: 'Número de administración debe tener menos de 3 caracteres' }),
    });

export  const userSchema = z.object({
        tipo: z.string(),
        dni: z.string().length(9, { message: 'DNI debe tener 9 caracteres' }),
        nombre: z.string({ message: 'Nombre es requerido' }).max(50, { message: 'Nombre debe tener menos de 50 caracteres' }),
        apellidos: z.string().nullable(),
        password1: z.string({ message: 'Contraseña es requerida' }).min(8, { message: 'Contraseña debe tener al menos 8 caracteres' }).max(30, { message: 'Contraseña debe tener menos de 30 caracteres' }),
        password2: z.string({ message: 'Confirmar contraseña es requerida' }).min(8, { message: 'Confirmar contraseña debe tener al menos 8 caracteres' }).max(30, { message: 'Confirmar contraseña debe tener menos de 30 caracteres' }),
        telefono: z.string({ message: 'Número de teléfono es requerido' }).length(9, { message: 'Número de teléfono debe tener 9 caracteres' }),
        email: z.string({ message: 'Email es requerido' }).email({ message: 'Email no es válido' })
    }).superRefine(({ password1, password2 }, ctx) => { if (password2 !== password1) { ctx.addIssue({ code: "custom", message: "Las contraseñas no coinciden.", path: ['password2'] }) } })
