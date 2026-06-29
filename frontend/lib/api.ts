import { AnalyzeResponse, AuthResponse, HistoryItem, MenuResponse, Profile, RecommendationResponse } from "@/lib/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
const DEFAULT_TIMEOUT_MS = 180000;

function getStoredUserId(): string | null {
  if (typeof window === "undefined") {
    return null;
  }

  return window.localStorage.getItem("platewise_user_id");
}

async function readApiError(response: Response, fallback: string): Promise<string> {
  try {
    const payload = await response.json();
    const detail = payload?.detail;
    if (typeof detail === "string") {
      return detail;
    }
    if (detail?.message && typeof detail.message === "string") {
      return detail.message;
    }
  } catch {
    return fallback;
  }

  return fallback;
}

export function persistAuthSession(auth: AuthResponse) {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.setItem("platewise_token", auth.access_token);
  window.localStorage.setItem("platewise_user_id", String(auth.user_id));
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const userId = getStoredUserId();
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS);
  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      ...init,
      signal: init?.signal ?? controller.signal,
      headers: {
        "Content-Type": "application/json",
        ...(userId ? { "X-User-Id": userId } : {}),
        ...(init?.headers ?? {})
      },
      cache: "no-store"
    });

    if (!response.ok) {
      throw new Error(await readApiError(response, `Request failed with status ${response.status}`));
    }

    return (await response.json()) as T;
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error("The request took too long. Try a clearer or shorter menu file.");
    }
    if (error instanceof Error) {
      throw error;
    }
    throw new Error("API unavailable");
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export async function signUp(email: string, password: string): Promise<AuthResponse> {
  return await request<AuthResponse>("/auth/signup", {
    method: "POST",
    body: JSON.stringify({ email, password })
  });
}

export async function login(email: string, password: string): Promise<AuthResponse> {
  return await request<AuthResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password })
  });
}

export async function fetchProfile(): Promise<Profile | null> {
  try {
    return await request<Profile | null>("/profile");
  } catch {
    return null;
  }
}

export async function saveProfile(profile: Profile): Promise<Profile> {
  try {
    return await request<Profile>("/profile", {
      method: "PUT",
      body: JSON.stringify(profile)
    });
  } catch {
    return profile;
  }
}

export async function ingestRestaurantUrl(url: string): Promise<MenuResponse> {
  return await request<MenuResponse>("/ingest/url", {
    method: "POST",
    body: JSON.stringify({ url })
  });
}

export async function fetchMenus(): Promise<MenuResponse[]> {
  try {
    return await request<MenuResponse[]>("/menus");
  } catch {
    return [];
  }
}

export async function fetchMenu(menuId: number): Promise<MenuResponse | null> {
  try {
    return await request<MenuResponse>(`/menus/${menuId}`);
  } catch {
    return null;
  }
}

export async function uploadMenu(file: File): Promise<{ upload_id: number; menu_id: number; extracted_preview: string }> {
  const formData = new FormData();
  formData.append("file", file);
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS);

  try {
    const response = await fetch(`${API_BASE_URL}/uploads`, {
      method: "POST",
      signal: controller.signal,
      headers: {
        ...(getStoredUserId() ? { "X-User-Id": getStoredUserId() as string } : {})
      },
      body: formData
    });

    if (!response.ok) {
      throw new Error(await readApiError(response, `Upload failed with status ${response.status}`));
    }

    return (await response.json()) as {
      upload_id: number;
      menu_id: number;
      extracted_preview: string;
    };
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error("The upload took too long. Try a clearer or shorter menu file.");
    }
    if (error instanceof Error) {
      throw error;
    }
    throw new Error("Upload failed");
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export async function analyzeMenu(file: File): Promise<AnalyzeResponse> {
  const formData = new FormData();
  formData.append("file", file);
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS);

  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: "POST",
      signal: controller.signal,
      headers: {
        ...(getStoredUserId() ? { "X-User-Id": getStoredUserId() as string } : {})
      },
      body: formData
    });

    if (!response.ok) {
      throw new Error(await readApiError(response, `Analyze failed with status ${response.status}`));
    }

    return (await response.json()) as AnalyzeResponse;
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error("Analysis took too long. Try a clearer or shorter menu file.");
    }
    if (error instanceof Error) {
      throw error;
    }
    throw new Error("Analyze failed");
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export async function fetchRecommendations(menuId: number): Promise<RecommendationResponse> {
  return await request<RecommendationResponse>(`/recommendations/${menuId}`, {
    method: "POST"
  });
}

export async function fetchHistory(): Promise<HistoryItem[]> {
  try {
    return await request<HistoryItem[]>("/history");
  } catch {
    return [];
  }
}

export async function setRecommendationSaved(
  recommendationId: number,
  saved: boolean
): Promise<HistoryItem> {
  return await request<HistoryItem>(`/history/${recommendationId}/save`, {
    method: "PUT",
    body: JSON.stringify({ saved })
  });
}
