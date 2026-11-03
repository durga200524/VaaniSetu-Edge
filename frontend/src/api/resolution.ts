import api from "./client";

export interface ResolutionPassport {
  passport_id: string;
  timestamp: string;

  customer_interaction?: {
    transcript?: string;
    language?: string;
    audio_analysis?: Record<string, unknown>;
  };

  intent_analysis?: {
    intent?: string;
    confidence?: number;
  };

  ai_resolution?: {
    response?: string;
    model?: string;
    knowledge_sources?: string[];
  };

  speech_output?: {
    model?: string;
    voice?: string;
    language?: string;
    audio_format?: string;
  };

  processing?: {
    status?: string;
    processing_time_seconds?: number;
  };
}

export interface ResolutionHistoryResponse {
  success: boolean;
  total_passports: number;
  passports: ResolutionPassport[];
}

export const getAllPassports = async (): Promise<ResolutionHistoryResponse> => {
  const response = await api.get<ResolutionHistoryResponse>(
    "/api/v1/resolution/all"
  );

  return response.data;
};