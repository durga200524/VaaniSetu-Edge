import api from "./client";

export interface HealthResponse {
  status: string;
  backend: string;
  project: string;
}

export const checkBackendHealth = async (): Promise<HealthResponse> => {
  const response = await api.get<HealthResponse>("/health");

  return response.data;
};