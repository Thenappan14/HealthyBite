import { HistoryItem, MenuResponse, Profile, RecommendationResponse } from "@/lib/types";

export const defaultProfile: Profile = {
  name: "Jordan Lee",
  age: 31,
  sex: "female",
  height_cm: 168,
  weight_kg: 64,
  activity_level: "moderately_active",
  primary_goal: "better_energy",
  diet_type: "pescatarian",
  allergies: ["peanuts"],
  disliked_foods: ["mushroom"],
  spice_preference: "medium",
  budget_preference: "moderate",
  preferred_cuisines: ["mediterranean", "japanese"]
};

export const sampleMenu: MenuResponse = {
  id: 1,
  source_type: "upload",
  source_filename: "sample_menu_upload.txt",
  extracted_text: "Sample extracted menu text",
  structured_json: {},
  items: [
    {
      id: 1,
      category: "Bowls",
      name: "Salmon Power Bowl",
      description: "Brown rice, kale, avocado, edamame, sesame dressing",
      price: 21,
      nutrition_estimate: {
        calories: 410,
        protein_g: 30,
        carbs_g: 12,
        fat_g: 18,
        fiber_g: 4,
        sugar_g: 4,
        sodium_mg: 520
      },
      allergens: ["fish", "sesame"],
      confidence_score: 0.85
    },
    {
      id: 2,
      category: "Bowls",
      name: "Tofu Harvest Bowl",
      description: "Quinoa, roasted squash, kale, tahini",
      price: 17,
      nutrition_estimate: {
        calories: 350,
        protein_g: 20,
        carbs_g: 18,
        fat_g: 14,
        fiber_g: 6,
        sugar_g: 4,
        sodium_mg: 480
      },
      allergens: ["soy", "sesame"],
      confidence_score: 0.82
    }
  ]
};

export const sampleRecommendations: RecommendationResponse = {
  disclaimer:
    "Recommendations are based on estimated nutrition and provided profile information. This is not medical advice.",
  top_recommendations: [
    {
      menu_item_id: 1,
      dish_name: "Salmon Power Bowl",
      category: "Bowls",
      match_score: 88.4,
      summary_reason: "Looks supportive for steady energy with likely fiber and meal substance.",
      nutrition_estimate: sampleMenu.items[0].nutrition_estimate,
      allergens: ["fish", "sesame"],
      warnings: ["Contains possible allergens based on likely ingredients and menu wording."],
      why_recommended: [
        "Looks supportive for steady energy with likely fiber and meal substance.",
        "Provides a likely solid protein serving.",
        "Estimated calories are in a practical meal range."
      ],
      why_not_recommended: ["Price looks above the stated budget preference."],
      recommendation_type: "top_pick"
    }
  ],
  alternatives: [],
  dishes_to_avoid: [
    {
      menu_item_id: 3,
      dish_name: "Chicken Fuel Bowl",
      category: "Bowls",
      match_score: 5,
      summary_reason: "Excluded for pescatarian compatibility.",
      nutrition_estimate: {},
      allergens: [],
      warnings: ["Excluded based on likely ingredients from the menu wording."],
      why_recommended: [],
      why_not_recommended: ["Does not appear compatible with a pescatarian diet."],
      recommendation_type: "avoid"
    }
  ]
};

export const sampleHistory: HistoryItem[] = [
  {
    id: 1,
    type: "top_pick",
    score: 88.4,
    dish_name: "Salmon Power Bowl",
    summary_reason: "Strong energy and protein fit based on menu information.",
    warnings: ["Contains fish and sesame."],
    saved: true,
    created_at: "2026-03-29T10:30:00Z"
  }
];

