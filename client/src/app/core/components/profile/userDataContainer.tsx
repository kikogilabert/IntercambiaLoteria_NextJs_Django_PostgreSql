import { Input, Button } from "@nextui-org/react"
import { MailIcon, Phone, UserRoundPenIcon } from "lucide-react";
import { UserProfileData, AdministracionProfileData } from "@/core/interfaces/user.interface";


export function PerfilContainer({ userData, onEdit }: { userData: UserProfileData, onEdit: () => void }) {
    return (
        <div className="w-full max-w-[375px] h-full flex flex-col gap-[18px] p-2 items-center justify-center">
            <h1>Datos personales</h1>
            <div className="w-full  h-full rounded border-1 p-3 flex flex-col gap-[8px]">
                <Input label="Tipo" isDisabled value={userData?.tipo}></Input>
                <Input label="Nombre" isDisabled value={userData?.nombre}></Input>
                <Input label="Apellidos" isDisabled value={userData?.apellidos}></Input>
                <Input label="DNI" isDisabled value={userData?.dni}></Input>
                <Input
                    label="Email"
                    isDisabled
                    type="email"
                    startContent={<MailIcon strokeWidth={2} size={"16px"} />}
                    value={userData?.email}
                ></Input>
                <Input label="Telefono" startContent={<Phone strokeWidth={2} size={"16px"} />} isDisabled value={userData?.telefono}></Input>
            </div>
            <div>
                <Button color="warning" onPress={onEdit} endContent={<UserRoundPenIcon size={"20px"} strokeWidth={2} />}>Editar</Button>
            </div>
        </div>
    );
}

export function AdmonContainer({ admonData, onEdit }: { admonData: AdministracionProfileData, onEdit: () => void }) {
    return (
        <div className="w-full max-w-[375px] h-full flex flex-col gap-[18px] p-2 items-center justify-center">
            <h1>Tu administracion</h1>
            <div className="w-full  h-full rounded border-1 p-3 flex flex-col gap-[8px]">
                <Input label="Nombre comercial" isDisabled value={admonData?.nombre_comercial}></Input>
                <Input label="Numero receptor" isDisabled value={admonData?.numero_receptor}></Input>
                <Input label="Dirección" isDisabled value={admonData?.direccion}></Input>
                <Input label="Localidad" isDisabled value={admonData?.localidad}></Input>
                <Input label="Codigo postal" isDisabled value={admonData?.codigo_postal}></Input>
                <Input label="Numero administracion" isDisabled value={admonData?.numero_administracion}></Input>
                <Input label="Provincia" isDisabled value={admonData?.provincia}></Input>
            </div>
            <div>
                <Button color="warning" onPress={onEdit} endContent={<UserRoundPenIcon size={"20px"} strokeWidth={2} />}>Editar</Button>
            </div>
        </div>
    );
}