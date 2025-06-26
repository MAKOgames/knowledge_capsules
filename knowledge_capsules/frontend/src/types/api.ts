// src/types/api.ts

// Этот файл определяет типы данных, которые используются
// при обмене информацией между frontend и backend.
// Они должны соответствовать Pydantic схемам на бэкенде.

// --- Capsule Types ---

export interface Capsule {
  id: number;
  owner_id: number;
  title: string | null;
  content: string;
  source_url: string | null;
  created_at: string; // Даты приходят как строки в формате ISO
  send_at: string;
  is_sent: boolean;
}

export interface CapsuleCreate {
  title?: string;
  content: string;
  source_url?: string;
  send_at: string; // Напр., "2025-12-31"
}

export interface CapsuleUpdate {
  title?: string;
  content?: string;
  source_url?: string;
  send_at?: string;
}

// --- User Types ---

export interface User {
  id: number;
  email: string;
  is_active: boolean;
  capsules: Capsule[];
}

export interface UserCreate {
  email: string;
  password: string;
}
