import { defaultProfile, sampleHistory, sampleMenu, sampleRecommendations } from "@/lib/mock-data";
import { HistoryItem, MenuResponse, Profile, RecommendationResponse } from "@/lib/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
const DEMO_USER_ID = process.env.NEXT_PUBLIC_DEMO_USER_ID ?? "1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        "X-User-Id": DEMO_USER_ID,
        ...(init?.headers ?? {})
      },
      cache: "no-store"
    });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    return (await response.json()) as T;
  } catch {
    throw new Error("API unavailable");
  }
}

export async function fetchProfile(): Promise<Profile> {
  try {
    const profile = await request<Profile | null>("/profile");
    return profile ?? defaultProfile;
  } catch {
    return defaultProfile;
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
  try {
    return await request<MenuResponse>("/ingest/url", {
      method: "POST",
      body: JSON.stringify({ url })
    });
  } catch {
    return sampleMenu;
  }
}

export async function uploadMenu(file: File): Promise<{ upload_id: number; menu_id: number; extracted_preview: string }> {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${API_BASE_URL}/uploads`, {
      method: "POST",
      headers: {
        "X-User-Id": DEMO_USER_ID
      },
      body: formData
    });

    if (!response.ok) {
      throw new Error(`Upload failed with status ${response.status}`);
    }

    return (await response.json()) as {
      upload_id: number;
      menu_id: number;
      extracted_preview: string;
    };
  } catch {
    return {
      upload_id: 1,
      menu_id: sampleMenu.id,
      extracted_preview: "Sample OCR extraction for uploaded menu."
    };
  }
}

export async function fetchRecommendations(menuId: number): Promise<RecommendationResponse> {
  try {
    return await request<RecommendationResponse>(`/recommendations/${menuId}`, {
      method: "POST"
    });
  } catch {
    return sampleRecommendations;
  }
}

export async function fetchHistory(): Promise<HistoryItem[]> {
  try {
    return await request<HistoryItem[]>("/history");
  } catch {
    return sampleHistory;
  }
}
