export type Profile = {
  id?: number;
  user_id?: number;
  name: string;
  age: number;
  sex: string;
  height_cm: number;
  weight_kg: number;
  activity_level: string;
  primary_goal: string;
  diet_type: string;
  allergies: string[];
  disliked_foods: string[];
  spice_preference: string;
  budget_preference: string;
  preferred_cuisines: string[];
};

export type MenuItem = {
  id: number;
  category?: string;
  name: string;
  description?: string;
  price?: number;
  nutrition_estimate: Record<string, number>;
  allergens: string[];
  warnings?: string[];
  confidence_score: number;
};

export type MenuResponse = {
  id: number;
  source_type: string;
  source_url?: string;
  source_filename?: string;
  extracted_text?: string;
  structured_json: Record<string, unknown>;
  items: MenuItem[];
};

export type Recommendation = {
  menu_item_id: number;
  dish_name: string;
  category?: string;
  match_score: number;
  summary_reason: string;
  nutrition_estimate: Record<string, number>;
  allergens: string[];
  warnings: string[];
  why_recommended: string[];
  why_not_recommended: string[];
  recommendation_type: string;
};

export type RecommendationResponse = {
  disclaimer: string;
  top_recommendations: Recommendation[];
  alternatives: Recommendation[];
  dishes_to_avoid: Recommendation[];
};

export type HistoryItem = {
  id: number;
  type: string;
  score: number;
  dish_name: string;
  summary_reason: string;
  warnings: string[];
  saved: boolean;
  created_at: string;
};

