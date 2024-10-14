"use client"
import { useAuth } from "@/core/context/auth.context"
import { UserProfileData, AdministracionProfileData } from "@/core/interfaces/user.interface";
import { Avatar, Button, CircularProgress, Input, Modal, ModalBody, ModalContent, ModalFooter, ModalHeader, useDisclosure, Tabs, Tab } from "@nextui-org/react";
import { CreditCard, MailIcon, Phone, UserRoundPenIcon } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { updateUserData, updateAdmonData } from "@/core/api/auth";
import useScreenDetector from "@/core/hooks/useScreenDetector";
import { CustomStorage } from "@/core/common/local-storage";
import { StorageVariables } from "@/core/constants";
import {PerfilContainer, AdmonContainer} from "@/core/components/profile/userDataContainer";


export default function ProfileContainer() {
    const auth = useAuth();
    const { isDesktop } = useScreenDetector();
    const [userToken, setUserToken] = useState<string>("");
    const [userData, setUserData] = useState<UserProfileData | undefined>();
    const [admonData, setAdmonData] = useState<AdministracionProfileData | undefined>();
    const [updatedData, setUpdatedData] = useState<any>({});
    const [editingSection, setEditingSection] = useState<string>("");

    const router = useRouter();
    const { isOpen, onOpen, onOpenChange, onClose } = useDisclosure();

    useEffect(() => {
        if (auth.user && auth.token && auth.admon) {
            setUserToken(auth.token);
            setAdmonData(auth.admon);
            setUserData(auth.user);
        } else {
            router.push("/iniciar-sesion");
        }
    }, [auth.user]);

    const handleEdit = (section: string) => {
        setEditingSection(section);
        if (section === 'personal') {
            setUpdatedData({ ...userData });
        } else if (section === 'administracion') {
            setUpdatedData({ ...admonData });
        }
        onOpen();
    };

    const handleSaveNewData = async () => {
        try {
            if (editingSection === 'personal') {
                if (JSON.stringify(updatedData) !== JSON.stringify(userData)) {
                    const response = await updateUserData(updatedData, userToken);
                    if (response.status === "success") {
                        setUserData((prevUserData) => ({ ...prevUserData, ...updatedData } as UserProfileData));
                        CustomStorage.setItem(StorageVariables.UserData, updatedData);
                    } else {
                        console.error("Error updating user data", response);
                    }
                }
            } else if (editingSection === 'administracion') {
                if (JSON.stringify(updatedData) !== JSON.stringify(admonData)) {
                    const response = await updateAdmonData(updatedData, userData!.administracion, userToken); //
                    if (response.status === "success") {
                        setAdmonData((prevAdmonData) => ({ ...prevAdmonData, ...updatedData } as AdministracionProfileData));
                        CustomStorage.setItem(StorageVariables.AdmonData, updatedData);
                    } else {
                        console.error("Error updating administration data", response);
                    }
                }
            }
        } catch (error) {
            console.error("Error en la solicitud: ", error);
        }
    };

    return (
        <div className="flex flex-col w-full h-full justify-center items-center gap-[24px] mt-10 overflow-y-scroll">
            <div className="flex flex-row items-center gap-2">
                <Avatar src="https://i.pravatar.cc/150?u=a04258114e29026708c" className="w-20 h-20 text-large" />
                <h1 className="font-xl">
                    Bienvenido a tu perfil <span className="font-bold font-xl">{userData?.nombre}</span>.
                </h1>
            </div>

            {userData ? (
                isDesktop ? (
                    <div className="w-full h-auto flex md:flex-row flex-col gap-[40px] items-center justify-center pb-10">
                        <PerfilContainer userData={userData} onEdit={() => handleEdit('personal')} />
                        {admonData && <AdmonContainer admonData={admonData} onEdit={() => handleEdit('administracion')} />}
                    </div>
                ) : (
                    <div className="w-full flex flex-col justify-center items-center">
                        <Tabs variant={"solid"} className="flex flex-row gap-4">
                            <Tab key="personales" title="Datos Personales" className="w-full px-2">
                                <PerfilContainer userData={userData} onEdit={() => handleEdit('personal')} />
                            </Tab>
                            {admonData && (
                                <Tab key="administracion" title="Mi Administracion" className="w-full px-2">
                                    <AdmonContainer admonData={admonData} onEdit={() => handleEdit('administracion')} />
                                </Tab>
                            )}
                        </Tabs>
                    </div>
                )
            ) : (
                <CircularProgress />
            )}

            <Modal
                isOpen={isOpen}
                onOpenChange={onOpenChange}
                placement={isDesktop ? "top-center" : "center"}
                size="sm"
            >
                <ModalContent>
                    {() => (
                        <>
                            <ModalHeader className="flex flex-col gap-1">Edita {editingSection === 'personal' ? 'tu perfil' : 'tu administracion'}</ModalHeader>
                            <ModalBody>
                                <div className="w-full max-w-[350px] h-full max-h-[600px] rounded border-1 p-3 flex flex-col gap-[8px]">
                                    {editingSection === 'personal' ? (
                                        <>
                                            <Input
                                                label="Nombre"
                                                autoFocus
                                                defaultValue={updatedData?.nombre}
                                                onChange={(e) => setUpdatedData({ ...updatedData, nombre: e.target.value })}
                                            ></Input>
                                            <Input
                                                label="Apellidos"
                                                defaultValue={updatedData?.apellidos}
                                                onChange={(e) => setUpdatedData({ ...updatedData, apellidos: e.target.value })}
                                            ></Input>
                                            <Input
                                                label="DNI"
                                                endContent={<CreditCard strokeWidth={2} size={"18px"} />}
                                                value={updatedData?.dni}
                                                onChange={(e) => setUpdatedData({ ...updatedData, dni: e.target.value })}
                                            ></Input>
                                            <Input
                                                label="Email"
                                                type="email"
                                                endContent={<MailIcon strokeWidth={2} size={"18px"} />}
                                                value={updatedData?.email}
                                                onChange={(e) => setUpdatedData({ ...updatedData, email: e.target.value })}
                                            ></Input>
                                            <Input
                                                label="Telefono"
                                                endContent={<Phone strokeWidth={2} size={"18px"} />}
                                                value={updatedData?.telefono}
                                                onChange={(e) => setUpdatedData({ ...updatedData, telefono: e.target.value })}
                                            ></Input>
                                        </>
                                    ) : (
                                        <>
                                            <Input
                                                label="Nombre comercial"
                                                autoFocus
                                                defaultValue={updatedData?.nombre_comercial}
                                                onChange={(e) => setUpdatedData({ ...updatedData, nombre_comercial: e.target.value })}
                                            ></Input>
                                            <Input
                                                label="Numero receptor"
                                                defaultValue={updatedData?.numero_receptor}
                                                onChange={(e) => setUpdatedData({ ...updatedData, numero_receptor: e.target.value })}
                                            ></Input>
                                            <Input
                                                label="Dirección"
                                                defaultValue={updatedData?.direccion}
                                                onChange={(e) => setUpdatedData({ ...updatedData, direccion: e.target.value })}
                                            ></Input>
                                            <Input
                                                label="Localidad"
                                                defaultValue={updatedData?.localidad}
                                                onChange={(e) => setUpdatedData({ ...updatedData, localidad: e.target.value })}
                                            ></Input>
                                            <Input
                                                label="Codigo postal"
                                                defaultValue={updatedData?.codigo_postal}
                                                onChange={(e) => setUpdatedData({ ...updatedData, codigo_postal: e.target.value })}
                                            ></Input>
                                            <Input
                                                label="Numero administracion"
                                                defaultValue={updatedData?.numero_administracion}
                                                onChange={(e) => setUpdatedData({ ...updatedData, numero_administracion: e.target.value })}
                                            ></Input>
                                            <Input
                                                label="Provincia"
                                                defaultValue={updatedData?.provincia}
                                                onChange={(e) => setUpdatedData({ ...updatedData, provincia: e.target.value })}
                                            ></Input>
                                        </>
                                    )}
                                </div>
                            </ModalBody>
                            <ModalFooter>
                                <Button color="danger" variant="flat" onClick={() => setUpdatedData(editingSection === 'personal' ? userData : admonData)} onPress={onClose}>
                                    Cancelar
                                </Button>
                                <Button color="primary" onClick={() => handleSaveNewData()} onPress={onClose}>
                                    Guardar Cambios
                                </Button>
                            </ModalFooter>
                        </>
                    )}
                </ModalContent>
            </Modal>
        </div>
    );
}
