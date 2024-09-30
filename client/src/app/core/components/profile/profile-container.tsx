"use client"
import { useAuth } from "@/core/context/auth.context"
import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { CircularProgress } from "@nextui-org/react";

export default function ProfileContainer() {
   const router = useRouter();
   const auth = useAuth();

    useEffect(() => {
        if (auth.token && auth.user) {
            console.log('user is LOGGED', auth.user);
            const userData = auth.user;
            console.log('userData', userData);
        } else {
            console.log('user is NOT LOGGED');
            router.push('/iniciar-sesion');
        }
    },[])


    return (
    <div>
        {auth.user && auth.token ? (
            <h1>Profile</h1>   
        ): (
            <div className="flex flex-col md:h-[990px] h-[600px] justify-center items-center">
                <CircularProgress size="lg" aria-label="Loading..."/>
            </div>
        )}
    </div>
)



}