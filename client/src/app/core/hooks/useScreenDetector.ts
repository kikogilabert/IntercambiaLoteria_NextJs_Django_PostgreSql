'use client';
import { useEffect, useState } from "react";

export default function useScreenDetector() {
    const [width, setWidth] = useState(0);    

    useEffect(() => {
        const handleWindowSizeChange = () => {
            setWidth(window.innerWidth);
        };

        handleWindowSizeChange();

        window.addEventListener("resize", handleWindowSizeChange);

        return () => {
            window.removeEventListener("resize", handleWindowSizeChange);
        };
    }, []);

    const isMobile = width <= 768;
    const isDesktop = width > 768;
    const isXL = width >= 1280;

    return { isMobile, isDesktop, isXL};
};