"use client";

import Image from 'next/image';
import { useState } from 'react';
import { Navbar, NavbarBrand, NavbarMenuToggle, NavbarMenu, NavbarMenuItem, NavbarContent, NavbarItem, Link, Button, Avatar, Dropdown, DropdownItem, DropdownMenu, DropdownTrigger } from "@nextui-org/react";
import useScreenDetector from '@core/hooks/useScreenDetector';
export default function HeaderComponent() {

  const [isLogged, setIsLogged] = useState(false);
  const { isMobile } = useScreenDetector();

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

  const UserArea = [
    {
      name: "Registrate",
      link: "/registro",

    },
    {
      name: "Incia Sesión",
      link: "/inicia-sesion",

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
              <Avatar
                isBordered
                as="button"
                className="transition-transform"
                color="secondary"
                name="Jason Hughes"
                size="sm"
                src="https://i.pravatar.cc/150?u=a042581f4e29026704d"
              />
            </DropdownTrigger>
            <DropdownMenu aria-label="Profile Actions" variant="flat">
              <DropdownItem key="profile" className="h-14 gap-2">
                <p className="font-semibold">Signed in as</p>
                <p className="font-semibold">zoey@example.com</p>
              </DropdownItem>
              <DropdownItem key="settings">My Settings</DropdownItem>
              <DropdownItem key="team_settings">Team Settings</DropdownItem>
              <DropdownItem key="analytics">Analytics</DropdownItem>
              <DropdownItem key="system">System</DropdownItem>
              <DropdownItem key="configurations">Configurations</DropdownItem>
              <DropdownItem key="help_and_feedback">Help & Feedback</DropdownItem>
              <DropdownItem key="logout" color="danger">
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
              <Button as={Link} size={isMobile ? 'sm': 'md'} color="primary" href="/inicia-sesion" variant="flat">
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