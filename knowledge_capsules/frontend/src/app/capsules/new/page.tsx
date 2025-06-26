"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { api } from "@/lib/api";

export default function NewCapsulePage() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [sourceUrl, setSourceUrl] = useState("");
  const [sendAt, setSendAt] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError("");
    setSuccess("");
    setIsLoading(true);

    try {
      await api.createCapsule({
        title: title || undefined, // Отправляем undefined если поле пустое
        content,
        source_url: sourceUrl || undefined,
        send_at: new Date(sendAt).toISOString(),
      });

      setSuccess("Капсула успешно создана!");
      // Очищаем форму
      setTitle("");
      setContent("");
      setSourceUrl("");
      setSendAt("");
      
      // Через 2 секунды перенаправляем на страницу запланированных
      setTimeout(() => {
        router.push("/capsules/scheduled");
      }, 2000);

    } catch (err: any) {
      console.error("Ошибка создания капсулы:", err);
      setError(err.message || "Не удалось создать капсулу.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Создать новую капсулу</CardTitle>
        <CardDescription>
          Заполните информацию ниже. Мы напомним вам об этой идее в будущем.
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="grid gap-6">
          <div className="grid gap-2">
            <Label htmlFor="title">Заголовок (необязательно)</Label>
            <Input
              id="title"
              placeholder="Напр., 'Ключевая идея о рефакторинге'"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              disabled={isLoading}
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="content">Содержание</Label>
            <Textarea
              id="content"
              placeholder="Сформулируйте главную мысль, которую хотите запомнить..."
              required
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={6}
              disabled={isLoading}
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="sourceUrl">URL источника (необязательно)</Label>
            <Input
              id="sourceUrl"
              type="url"
              placeholder="https://example.com/article"
              value={sourceUrl}
              onChange={(e) => setSourceUrl(e.target.value)}
              disabled={isLoading}
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="sendAt">Дата напоминания</Label>
            <Input
              id="sendAt"
              type="date"
              required
              value={sendAt}
              onChange={(e) => setSendAt(e.target.value)}
              disabled={isLoading}
            />
          </div>
          {error && <p className="text-sm text-red-500">{error}</p>}
          {success && <p className="text-sm text-green-600">{success}</p>}
        </CardContent>
        <CardFooter className="border-t px-6 py-4">
          <Button type="submit" disabled={isLoading}>
            {isLoading ? 'Сохранение...' : 'Сохранить капсулу'}
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}
