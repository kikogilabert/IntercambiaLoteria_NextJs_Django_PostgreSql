import type { Metadata } from "next";
import "./globals.css";
import { NextUIProvider } from "@nextui-org/react";
import HeaderComponent from "./core/components/statics/Header/HeaderComponent";

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
          <NextUIProvider>
            <HeaderComponent />
          {children}
          {/* <FooterComponent /> */}
          </NextUIProvider>
      </body>
    </html>
  );
}
