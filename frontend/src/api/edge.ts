import api from "./client";

export interface EdgeSimulationRequest {
  available_ram_mb: number;
  cpu_cores: number;
  network_latency_ms: number;
  bandwidth_mbps: number;
  internet_available: boolean;
}

export interface EdgeSimulationResponse {
  success: boolean;
  simulation: string;

  input_resources: {
    available_ram_mb: number;
    cpu_cores: number;
    network_latency_ms: number;
    bandwidth_mbps: number;
    internet_available: boolean;
  };

  resource_assessment: {
    ram: string;
    cpu: string;
    network_latency: string;
    network_bandwidth: string;
    connectivity: string;
  };

  overall_status: string;
  limitations: string[];
  recommendations: string[];
  simulation_note: string;
}

export const simulateEdge = async (
  data: EdgeSimulationRequest
): Promise<EdgeSimulationResponse> => {
  const response = await api.post<EdgeSimulationResponse>(
    "/api/v1/edge/simulate",
    data
  );

  return response.data;
};