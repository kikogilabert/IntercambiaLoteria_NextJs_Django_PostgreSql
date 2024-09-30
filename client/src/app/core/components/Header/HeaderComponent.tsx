"use client";

import Image from 'next/image';
import { useEffect, useState } from 'react';
import { Navbar, NavbarBrand, NavbarMenuToggle, NavbarMenu, NavbarMenuItem, NavbarContent, NavbarItem, Link, Button, Avatar, Dropdown, DropdownItem, DropdownMenu, DropdownTrigger, User } from "@nextui-org/react";
import useScreenDetector from '@core/hooks/useScreenDetector';
import { useAuth } from '@/core/context/auth.context';
import { UserProfileData } from '@/core/interfaces/user.interface';
import { useRouter } from 'next/navigation';
export default function HeaderComponent() {
  //can get from this fuction the: 
  //userData = auth.user
  // token = auth.token  ->  jwt token from the user logged
  // auth.logOut  -> function to loggout 
  // auth.setLogin ->  function to set the user logged 
  const auth = useAuth();
  const router = useRouter();


  const [isLogged, setIsLogged] = useState(false);
  const [userData, setUserData] = useState<UserProfileData | null>(null);
  const { isMobile } = useScreenDetector();

  const handleLogout = () => {
    auth.logOut();
    setIsLogged(false);
    router.push('/iniciar-sesion');
  }

  useEffect(() => {
    if (auth.user && auth.token){ 
      console.log('user is LOGGED', auth.user);
      setUserData(auth.user);
      setIsLogged(true);
    }
  
  }, [auth.user, auth.token]);

  useEffect(() => {
    if (userData) {
      setIsLogged(true);
    }
  }, [userData]);

  const menuItems = [
    "Profile",
    "Dashboard",
    "Activity",
    "Analytics",
    "System",
    "Deployments",
    "My Settings",
    "Team Settings",
    "Help & Feedback",
    "Log Out",
  ];

  const NavbarItems = [
    {
      name: "Intercambios",
      link: "/intercambios",

    },
    {
      name: "Administraciones",
      link: "/Administraciones",

    },
    {
      name: "Sorteos",
      link: "/Sorteos",

    },
    {
      name: "Sobre nosotros",
      link: "/sobre-nosotros",
    }
  ];

  return (
    <Navbar isBordered>
      <NavbarContent className="sm:hidden" justify="start">
        <NavbarMenuToggle />
      </NavbarContent>

      <NavbarContent className="sm:hidden pr-3" justify="center">
        <NavbarBrand className='gap-2'>
          <Image src="/favicon.ico" alt="favicon for now" width={32} height={32} />
          {/* <p className="font-bold text-inherit">ConectaLoteria</p> */}
        </NavbarBrand>
      </NavbarContent>

      <NavbarContent className="hidden sm:flex gap-4" justify="center">
        <NavbarBrand>
          <Image src="/favicon.ico" alt="favicon for now" width={32} height={32} />
          {/* <p className="font-bold text-inherit">ConectaLoteria</p> */}
        </NavbarBrand>
        <NavbarContent className='hidden sm:flex gap-6' justify="center">
          {
            NavbarItems.map((item, index) => (
              <NavbarItem key={index}> {/* isActive={items} */}
                <Link color="foreground" href={item.link}>
                  {item.name}
                </Link>
              </NavbarItem>
            ))
          }
          {/* <NavbarItem>
                      <Link color="foreground" href="#">
                          Features
                      </Link>
                  </NavbarItem>
                  <NavbarItem isActive>
                      <Link href="#" aria-current="page" color="primary">
                          Customers
                      </Link>
                  </NavbarItem>
                  <NavbarItem>
                      <Link color="foreground" href="#">
                          Integrations
                      </Link>
                  </NavbarItem> */}
        </NavbarContent>
      </NavbarContent>

      <NavbarContent as="div" justify="end">
        {isLogged ? (
          <Dropdown placement="bottom-end">
            <DropdownTrigger>
            <User   
                name={userData?.nombre}
                description={userData?.email}
                avatarProps={{
                  src: "https://i.pravatar.cc/150?u=a04258114e29026702d",
                  showFallback : true
                }}
              />
            </DropdownTrigger>
            <DropdownMenu aria-label="Profile Actions" variant="flat">
              <DropdownItem key="profile" className="h-14 gap-2">
                <p className="font-semibold">Signed in as</p>
                <p className="font-bold">{userData?.email}</p>
              </DropdownItem>
              <DropdownItem key="user_profile" href='/perfil'>Mi Perfil</DropdownItem>
              <DropdownItem key="administracion">Mi administracion</DropdownItem>
              <DropdownItem key="intercambios">Mis intercambios</DropdownItem>
              <DropdownItem key="configurations">Ajustes</DropdownItem>
              <DropdownItem key="help_and_feedback">Ayuda & Atencion al Cliente</DropdownItem>
              <DropdownItem key="logout" color="danger" onClick={ () => handleLogout()}>
                Cerrar Sesión
              </DropdownItem>
            </DropdownMenu>
          </Dropdown>

        ) : (
          <>
            <NavbarItem className="hidden lg:flex">
              <Link href="/registro">Registrate</Link>
            </NavbarItem>
            <NavbarItem>
              <Button as={Link} size={isMobile ? 'sm': 'md'} color="primary" href="/iniciar-sesion" variant="flat">
                Inicia Sesión
              </Button>
            </NavbarItem>
          </>
        )
        }
      </NavbarContent>


      <NavbarMenu>
        {menuItems.map((item, index) => (
          <NavbarMenuItem key={`${item}-${index}`}>
            <Link
              className="w-full"
              color={
                index === 2 ? "warning" : index === menuItems.length - 1 ? "danger" : "foreground"
              }
              href="#"
              size="lg"
            >
              {item}
            </Link>
          </NavbarMenuItem>
        ))}
      </NavbarMenu>
    </Navbar>
  );

}