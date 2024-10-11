"use client"
import { useAuth } from "@/core/context/auth.context"
import { UserProfileData } from "@/core/interfaces/user.interface";
import { Avatar, Button, Checkbox, CircularProgress, Input, Modal, ModalBody, ModalContent, ModalFooter, ModalHeader, useDisclosure, Tabs, Tab } from "@nextui-org/react";
import { CreditCard, Link, LockIcon, MailIcon, Pencil, Phone, PhoneCallIcon, Underline, User, UserRoundPenIcon } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { UsuarioTypeEnum } from "@/core/interfaces/user.interface";
import { updateUserData } from "@/core/api/auth";
import useScreenDetector from "@/core/hooks/useScreenDetector";

export default function ProfileContainer() {

    const auth = useAuth();
    const { isDesktop } = useScreenDetector();
    const [userToken, setUserToken] = useState<string>("");
    const [userData, setUserData] = useState<UserProfileData>();
    const [updatedUserData, setupdatedUserData] = useState<any>({
    });


    const router = useRouter();
    const { isOpen, onOpen, onOpenChange, onClose } = useDisclosure();

    useEffect(() => {
        if (auth.user && auth.token) {
            setUserToken(auth.token);
            console.log('user is LOGGED', auth.user);
            setUserData(auth.user);
            setupdatedUserData({
                nombre: auth.user.nombre,
                apellidos: auth.user.apellidos,
                dni: auth.user.dni,
                email: auth.user.email,
                telefono: auth.user.telefono
            })
        } else {
            router.push('/iniciar-sesion')
        }
    }, [auth.user])

    const handleSaveNewUserData = async () => {
        console.log('updateUserData', updatedUserData);
        if (updatedUserData !== userData) {
            setUserData(prevUserData => ({ ...prevUserData, ...updatedUserData }));
            const response = await updateUserData(updatedUserData, userToken);
            console.log('response', response);
        } else {
            return;
        }
    }

    return (
        <div className="flex flex-col w-full h-full justify-center items-center gap-[24px] mt-10 overflow-y-scroll">
            <div className="flex flex-row items-center gap-2">
                <Avatar src="https://i.pravatar.cc/150?u=a04258114e29026708c" className="w-20 h-20 text-large" />
                <h1 className="font-xl">Bienvenido a tu perfil <span className="font-bold font-xl">{userData?.nombre}</span>.</h1>
            </div>

            {userData ?
                <>
                    {
                        isDesktop ? (
                            <div className="w-full h-auto flex md:flex-row flex-col gap-[40px] items-center justify-center pb-10" >
                                <div className="w-full max-w-[375px] h-full flex flex-col gap-[18px] p-2 items-center justify-center">
                                    <h1>Datos personales</h1>
                                    <div className="w-full  h-full rounded border-1 p-3 flex flex-col gap-[8px]">
                                        <Input label="Nombre" isDisabled value={userData?.nombre}></Input>
                                        <Input label="Apellidos" isDisabled value={userData?.apellidos}> </Input>
                                        <Input label="DNI" startContent={
                                            <CreditCard strokeWidth={2} size={"16px"} />
                                        } isDisabled value={userData?.dni}></Input>
                                        <Input
                                            label="Email"
                                            isDisabled type="email"
                                            startContent={
                                                <MailIcon strokeWidth={2} size={"16px"} />}
                                            value={userData?.email}></Input>
                                        <Input label="Telefono" startContent={<Phone strokeWidth={2} size={"16px"} />} isDisabled value={userData?.telefono}></Input>
                                    </div>
                                    <div>
                                        <Button color="warning" onPress={onOpen} endContent={<UserRoundPenIcon size={"20px"} strokeWidth={2} />}>Editar</Button>
                                    </div>
                                </div>
                                <div className="w-full max-w-[375px] h-full flex flex-col gap-[18px] p-2 items-center justify-center">
                                    <h1>Tu administracion:</h1>
                                    <div className="w-full  h-full rounded border-1 p-3 flex flex-col gap-[8px]">
                                        <Input label="Nombre" isDisabled value={userData?.nombre}></Input>
                                        <Input label="Apellidos" isDisabled value={userData?.apellidos}> </Input>
                                        <Input label="DNI" startContent={
                                            <CreditCard strokeWidth={2} size={"16px"} />
                                        } isDisabled value={userData?.dni}></Input>
                                        <Input
                                            label="Email"
                                            isDisabled type="email"
                                            startContent={
                                                <MailIcon strokeWidth={2} size={"16px"} />}
                                            value={userData?.email}></Input>
                                        <Input label="Telefono" startContent={<Phone strokeWidth={2} size={"16px"} />} isDisabled value={userData?.telefono}></Input>
                                    </div>
                                    <div>
                                        <Button color="warning" onPress={onOpen} endContent={<UserRoundPenIcon size={"20px"} strokeWidth={2} />}>Editar</Button>
                                    </div>
                                </div>

                            </div>) :
                            (
                                <div className="w-full flex flex-col justify-center items-center">
                                    <Tabs variant={"solid"} className="flex flex-row gap-4">
                                        <Tab key="personales" title="Datos Personales" className="w-full px-2">
                                            <div className="w-full h-full flex flex-col gap-[18px] p-2 items-center justify-center">
                                                <div className="w-full  h-full rounded border-1 p-3 flex flex-col gap-[8px]">
                                                    <Input label="Nombre" isDisabled value={userData?.nombre}></Input>
                                                    <Input label="Apellidos" isDisabled value={userData?.apellidos}> </Input>
                                                    <Input label="DNI" startContent={
                                                        <CreditCard strokeWidth={2} size={"16px"} />
                                                    } isDisabled value={userData?.dni}></Input>
                                                    <Input
                                                        label="Email"
                                                        isDisabled type="email"
                                                        startContent={
                                                            <MailIcon strokeWidth={2} size={"16px"} />}
                                                        value={userData?.email}></Input>
                                                    <Input label="Telefono" startContent={<Phone strokeWidth={2} size={"16px"} />} isDisabled value={userData?.telefono}></Input>
                                                </div>
                                                <div>
                                                    <Button color="warning" onPress={onOpen} endContent={<UserRoundPenIcon size={"20px"} strokeWidth={2} />}>Editar</Button>
                                                </div>
                                            </div>
                                        </Tab>
                                        <Tab key="administracion" title="Mi Administracion" className="w-full px-2">
                                            <div className="w-full h-full flex flex-col gap-[18px] p-2 items-center justify-center">
                                                <div className="w-full  h-full rounded border-1 p-3 flex flex-col gap-[8px]">
                                                    <Input label="Nombre" isDisabled value={userData?.nombre}></Input>
                                                    <Input label="Apellidos" isDisabled value={userData?.apellidos}> </Input>
                                                    <Input label="DNI" startContent={
                                                        <CreditCard strokeWidth={2} size={"16px"} />
                                                    } isDisabled value={userData?.dni}></Input>
                                                    <Input
                                                        label="Email"
                                                        isDisabled type="email"
                                                        startContent={
                                                            <MailIcon strokeWidth={2} size={"16px"} />}
                                                        value={userData?.email}></Input>
                                                    <Input label="Telefono" startContent={<Phone strokeWidth={2} size={"16px"} />} isDisabled value={userData?.telefono}></Input>
                                                </div>
                                                <div>
                                                    <Button color="warning" onPress={onOpen} endContent={<UserRoundPenIcon size={"20px"} strokeWidth={2} />}>Editar</Button>
                                                </div>
                                            </div>
                                        </Tab>
                                    </Tabs>
                                </div>

                            )
                    }</>

                : <CircularProgress />
            }







            <Modal
                isOpen={isOpen}
                onOpenChange={onOpenChange}
                placement={isDesktop ? "top-center" : "center"}
                size="sm"
            >
                <ModalContent>
                    {(onClose) => (
                        <>
                            <ModalHeader className="flex flex-col gap-1">Edita tu perfil</ModalHeader>
                            <ModalBody>
                                <div className="w-full max-w-[350px] h-full max-h-[600px] rounded border-1 p-3 flex flex-col gap-[8px]">
                                    <Input label="Nombre" autoFocus defaultValue={updatedUserData?.nombre} onChange={(e) => setupdatedUserData({ ...updatedUserData, nombre: e.target.value })}></Input>
                                    <Input label="Apellidos" defaultValue={updatedUserData?.apellidos} onChange={(e) => setupdatedUserData({ ...updatedUserData, apellidos: e.target.value })}> </Input>
                                    <Input label="DNI" endContent={
                                        <CreditCard strokeWidth={2} size={"18px"} />
                                    } value={updatedUserData?.dni} onChange={(e) => setupdatedUserData({ ...updatedUserData, dni: e.target.value })}></Input>
                                    <Input
                                        label="Email"
                                        type="email"
                                        endContent={
                                            <MailIcon strokeWidth={2} size={"18px"} />}
                                        value={userData?.email} onChange={(e) => setupdatedUserData({ ...updatedUserData, email: e.target.value })}></Input>
                                    <Input label="Telefono" endContent={<Phone strokeWidth={2} size={"18px"} />} value={updatedUserData?.telefono} onChange={(e) => setupdatedUserData({ ...updatedUserData, telefono: e.target.value })}></Input>
                                </div>
                            </ModalBody>
                            <ModalFooter>
                                <Button color="danger" variant="flat" onClick={() => setupdatedUserData(userData)} onPress={onClose}>
                                    Cancelar
                                </Button>
                                <Button color="primary" onPress={onClose} onClick={() => handleSaveNewUserData()}>
                                    Guardar Cambios
                                </Button>
                            </ModalFooter>
                        </>
                    )}
                </ModalContent>
            </Modal>
        </div >
    )



}
