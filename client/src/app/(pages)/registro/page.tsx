'use server';
import { getProvinciasRegister } from "@/core/api/data";
import RegisterComponent from "../../core/components/register/register_form"

export default async function Register() {
    
    let lista_provincias: any[] = await getProvinciasRegister();
    return (   
        <div className="flex flex-col justify-center align-center h-full w-full p-[25px] gap-4 pb-10">
            <RegisterComponent lista_comunidades={lista_provincias}/>
        </div>
    );
}
