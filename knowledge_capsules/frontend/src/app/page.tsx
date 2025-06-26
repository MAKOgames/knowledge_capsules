import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-slate-50 text-center p-4">
      <main className="max-w-3xl">
        <h1 className="text-4xl md:text-6xl font-bold text-slate-800">
          Запоминайте то, что действительно важно.
        </h1>
        <p className="mt-6 text-lg md:text-xl text-slate-600">
          «Капсулы Знаний» — это ваш личный помощник, который возвращает ключевые идеи из прочитанных статей и просмотренных видео именно тогда, когда вы начинаете их забывать. Превратите пассивное потребление контента в активное знание.
        </p>
        <div className="mt-8 flex justify-center gap-4">
          <Button asChild size="lg">
            <Link href="/signup">Начать бесплатно</Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link href="/login">Войти</Link>
          </Button>
        </div>
      </main>
      <footer className="absolute bottom-8 text-slate-500">
        <p>&copy; {new Date().getFullYear()} Капсулы Знаний. Все права защищены.</p>
      </footer>
    </div>
  );
}
