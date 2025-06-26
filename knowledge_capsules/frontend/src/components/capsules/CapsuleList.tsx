"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { MoreHorizontal } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

// TODO: Define a proper type for capsules
interface Capsule {
  id: number;
  title: string;
  status: 'scheduled' | 'sent';
  date: string;
}

interface CapsuleListProps {
  capsules: Capsule[];
}

export function CapsuleList({ capsules }: CapsuleListProps) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Название</TableHead>
          <TableHead>Статус</TableHead>
          <TableHead className="text-right">Дата</TableHead>
          <TableHead>
            <span className="sr-only">Действия</span>
          </TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {capsules.length > 0 ? (
          capsules.map((capsule) => (
            <TableRow key={capsule.id}>
              <TableCell className="font-medium">{capsule.title}</TableCell>
              <TableCell>{capsule.status === 'scheduled' ? 'Запланировано' : 'Отправлено'}</TableCell>
              <TableCell className="text-right">{capsule.date}</TableCell>
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
                    <DropdownMenuItem>Редактировать</DropdownMenuItem>
                    <DropdownMenuItem className="text-red-600">
                      Удалить
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))
        ) : (
          <TableRow>
            <TableCell colSpan={4} className="h-24 text-center">
              Нет капсул для отображения.
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  );
}
