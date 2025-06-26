import Link from "next/link";

export function Footer() {
  return (
    <footer className="bg-slate-100 border-t">
      <div className="container mx-auto py-6 px-4 md:px-6 flex flex-col md:flex-row items-center justify-between">
        <p className="text-sm text-slate-600">
          &copy; {new Date().getFullYear()} Капсулы Знаний. Все права защищены.
        </p>
        <nav className="flex gap-4 sm:gap-6 mt-4 md:mt-0">
          <Link href="/terms" className="text-sm text-slate-600 hover:underline underline-offset-4">
            Условия использования
          </Link>
          <Link href="/privacy" className="text-sm text-slate-600 hover:underline underline-offset-4">
            Политика конфиденциальности
          </Link>
        </nav>
      </div>
    </footer>
  );
}
