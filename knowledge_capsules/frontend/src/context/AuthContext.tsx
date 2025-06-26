"use client";

import { createContext, useContext, useState, ReactNode } from "react";
import { api } from "@/lib/api";
import { UserCreate } from "@/types/api";

interface AuthContextType {
  login: (formData: FormData) => Promise<void>;
  signup: (data: UserCreate) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(
    typeof window !== "undefined" ? localStorage.getItem("token") : null
  );

  const login = async (formData: FormData) => {
    const resp = await api.login(formData);
    setToken(resp.access_token);
  };

  const signup = async (data: UserCreate) => {
    await api.signup(data);
  };

  const value: AuthContextType = { login, signup };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}
