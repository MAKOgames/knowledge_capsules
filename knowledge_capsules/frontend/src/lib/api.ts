// src/lib/api.ts

import {
  User,
  UserCreate,
  Capsule,
  CapsuleCreate,
  CapsuleUpdate,
} from "@/types/api"; // Предполагается, что у вас есть файл с типами

const API_URL = process.env.NEXT_PUBLIC_API_URL;

type TokenResponse = {
  access_token: string;
  token_type: string;
};

// --- Helper Functions ---

async function fetcher<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_URL}${endpoint}`;
  
  // Получаем токен из localStorage, если он есть
  const token = localStorage.getItem("token");
  
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(url, { ...options, headers });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const errorMessage = errorData.detail || `Ошибка API: ${response.statusText}`;
    throw new Error(errorMessage);
  }

  // Для запросов, которые не возвращают тело (напр. DELETE)
  if (response.status === 204) {
    return null as T;
  }

  return response.json();
}

// --- Auth API ---

export const api = {
  login: async (formData: FormData): Promise<TokenResponse> => {
    const response = await fetcher<TokenResponse>(`/auth/login/access-token`, {
      method: "POST",
      body: formData,
      headers: {
        // 'Content-Type' здесь устанавливается браузером автоматически для FormData
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
    // Сохраняем токен в localStorage
    if (response.access_token) {
      localStorage.setItem("token", response.access_token);
    }
    return response;
  },

  signup: (data: UserCreate): Promise<User> => {
    return fetcher<User>("/auth/signup", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  getMe: (): Promise<User> => {
    return fetcher<User>("/auth/me");
  },

  // --- Capsules API ---

  getCapsules: (): Promise<Capsule[]> => {
    return fetcher<Capsule[]>("/capsules/");
  },

  createCapsule: (data: CapsuleCreate): Promise<Capsule> => {
    return fetcher<Capsule>("/capsules/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  updateCapsule: (id: number, data: CapsuleUpdate): Promise<Capsule> => {
    return fetcher<Capsule>(`/capsules/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  deleteCapsule: (id: number): Promise<void> => {
    return fetcher<void>(`/capsules/${id}`, {
      method: "DELETE",
    });
  },
};
