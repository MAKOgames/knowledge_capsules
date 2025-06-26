"use client";

import { useEffect, useState } from "react";
import { MoreHorizontal } from "lucide-react";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";
import { Capsule } from "@/types/api";

export default function SentCapsulesPage() {
  const [capsules, setCapsules] = useState<Capsule[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCapsules = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const allCapsules = await api.getCapsules();
      const sent = allCapsules.filter(c => c.is_sent);
      setCapsules(sent);
    } catch (err: any) {
      setError("Не удалось загрузить капсулы.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCapsules();
  }, []);

  const handleDelete = async (capsuleId: number) => {
    // TODO: В Фазе 3 добавить модальное окно для подтверждения удаления.
    try {
      await api.deleteCapsule(capsuleId);
      // Обновляем список капсул, удаляя из него удаленную.
      fetchCapsules();
    } catch (err: any) {
      console.error("Ошибка удаления капсулы:", err);
      // В Фазе 3 можно будет добавить уведомление об ошибке.
      alert("Не удалось удалить капсулу.");
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU');
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Отправленные капсулы</CardTitle>
        <CardDescription>
          Здесь находится ваш архив уже отправленных напоминаний.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Название</TableHead>
              <TableHead className="hidden md:table-cell">Статус</TableHead>
              <TableHead className="text-right">Дата отправки</TableHead>
              <TableHead>
                <span className="sr-only">Действия</span>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell colSpan={4} className="h-24 text-center">
                  Загрузка...
                </TableCell>
              </TableRow>
            ) : error ? (
               <TableRow>
                <TableCell colSpan={4} className="h-24 text-center text-red-500">
                  {error}
                </TableCell>
              </TableRow>
            ) : capsules.length > 0 ? (
              capsules.map((capsule) => (
                <TableRow key={capsule.id}>
                  <TableCell className="font-medium">{capsule.title || 'Без названия'}</TableCell>
                   <TableCell className="hidden md:table-cell">
                    <Badge variant="secondary">Отправлено</Badge>
                  </TableCell>
                  <TableCell className="text-right">{formatDate(capsule.send_at)}</TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button aria-haspopup="true" size="icon" variant="ghost">
                          <MoreHorizontal className="h-4 w-4" />
                          <span className="sr-only">Toggle menu</span>
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Действия</DropdownMenuLabel>
                        <DropdownMenuItem
                          onSelect={() => handleDelete(capsule.id)}
                          className="text-red-500 focus:text-red-500 focus:bg-red-50"
                        >
                          Удалить
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={4} className="text-center h-24">
                  Нет отправленных капсул.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}
