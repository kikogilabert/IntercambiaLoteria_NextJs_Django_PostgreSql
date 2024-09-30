import type { Metadata } from "next";
import "./globals.css";
import { NextUIProvider } from "@nextui-org/react";
import HeaderComponent from "./core/components/statics/Header/HeaderComponent";
import AuthProvider from "./core/context/auth.context";

export const metadata: Metadata = {
  title: "ConectaLoteria",
  description: "ConectaLoteria es una plataforma creada para conectar administraciones de lotería para intercambiar de loteria.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="">
        <AuthProvider>
          <NextUIProvider>
            <HeaderComponent />
          {children}
          {/* <FooterComponent /> */}
          </NextUIProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
