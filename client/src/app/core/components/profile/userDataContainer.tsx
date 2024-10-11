import { CircularProgress, Input } from "@nextui-org/react"
import { CreditCard, MailIcon, Phone } from "lucide-react"

export default function userDataContainerForm(userData: any) {




    return (
        <div className="w-full max-w-[350px] h-full max-h-[600px] rounded border-1 p-3 flex flex-col gap-[8px]">
        <Input label="Nombre" isDisabled value={userData?.nombre}></Input>
        <Input label="Apellidos" isDisabled value={userData?.apellidos}> </Input>
        <Input label="DNI" startContent={
            <CreditCard  strokeWidth={2} size={"16px"}/>
        } isDisabled value={userData?.dni}></Input>
        <Input
        label="Email"
        isDisabled type="email"
            startContent={ 
                <MailIcon strokeWidth={2} size={"16px"} />} 
            value={userData?.email}></Input>
        <Input label="Telefono" startContent={<Phone strokeWidth={2} size={"16px"} />} isDisabled value={userData?.telefono}></Input>
    </div>
    )
}