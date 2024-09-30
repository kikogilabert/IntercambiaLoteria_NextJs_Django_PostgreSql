import { Link } from '@nextui-org/react';

export default function FooterComponent() {

return (
    <footer className="bg-zinc-900 text-white py-6 fixed bottom-0 w-full">
      <div className="container mx-auto flex flex-col md:flex-row justify-between items-center">
        <div className="mb-4 md:mb-0">
          <h2 className="text-xl font-bold">Mi Proyecto</h2>
          <p className="text-sm">© 2024 Mi Proyecto. Todos los derechos reservados.</p>
        </div>
        <div className="flex space-x-6">
          <Link href="/" className="text-white hover:text-gray-400">
            Inicio
          </Link>
          <Link href="/about" className="text-white hover:text-gray-400">
            Sobre Nosotros
          </Link>
          <Link href="/contact" className="text-white hover:text-gray-400">
            Contacto
          </Link>
        </div>
      </div>
    </footer>
  );
}