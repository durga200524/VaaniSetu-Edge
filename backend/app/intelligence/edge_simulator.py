from typing import Optional


def simulate_edge_constraints(
    available_ram_mb: float = 512,
    cpu_cores: float = 2,
    network_latency_ms: float = 100,
    bandwidth_mbps: float = 10,
    internet_available: bool = True
):
    """
    Simulate VaaniSetu Edge under limited device
    resources and network conditions.

    This is a software simulation. It does not
    change the actual computer's hardware resources.
    """

    if available_ram_mb <= 0:
        raise ValueError("Available RAM must be greater than zero.")

    if cpu_cores <= 0:
        raise ValueError("CPU cores must be greater than zero.")

    if network_latency_ms < 0:
        raise ValueError("Network latency cannot be negative.")

    if bandwidth_mbps < 0:
        raise ValueError("Bandwidth cannot be negative.")

    # RAM assessment
    if available_ram_mb < 256:
        ram_status = "CRITICAL"
    elif available_ram_mb < 512:
        ram_status = "LOW"
    else:
        ram_status = "SUFFICIENT"

    # CPU assessment
    if cpu_cores < 1:
        cpu_status = "CRITICAL"
    elif cpu_cores < 2:
        cpu_status = "LIMITED"
    else:
        cpu_status = "SUFFICIENT"

    # Network latency assessment
    if network_latency_ms > 1000:
        latency_status = "VERY HIGH"
    elif network_latency_ms > 300:
        latency_status = "HIGH"
    else:
        latency_status = "NORMAL"

    # Bandwidth assessment
    if bandwidth_mbps == 0:
        bandwidth_status = "UNAVAILABLE"
    elif bandwidth_mbps < 1:
        bandwidth_status = "VERY LOW"
    elif bandwidth_mbps < 5:
        bandwidth_status = "LOW"
    else:
        bandwidth_status = "SUFFICIENT"

    # Connectivity assessment
    if not internet_available:
        connectivity_status = "OFFLINE"
    else:
        connectivity_status = "ONLINE"

    # Identify operational limitations
    limitations = []
    recommendations = []

    if ram_status in ["CRITICAL", "LOW"]:
        limitations.append("Limited memory availability.")
        recommendations.append(
            "Use lightweight models and reduce memory usage."
        )

    if cpu_status in ["CRITICAL", "LIMITED"]:
        limitations.append("Restricted CPU processing capacity.")
        recommendations.append(
            "Reduce computational workload."
        )

    if latency_status in ["HIGH", "VERY HIGH"]:
        limitations.append("High network communication delay.")
        recommendations.append(
            "Use local processing where possible."
        )

    if bandwidth_status in ["LOW", "VERY LOW"]:
        limitations.append("Limited network bandwidth.")
        recommendations.append(
            "Compress audio before transmission."
        )

    if connectivity_status == "OFFLINE":
        limitations.append("Internet connection is unavailable.")
        recommendations.append(
            "Use cached knowledge and offline capabilities."
        )

    # Overall simulation status
    if (
        ram_status == "CRITICAL"
        or cpu_status == "CRITICAL"
        or connectivity_status == "OFFLINE"
    ):
        overall_status = "SEVERE CONSTRAINTS"

    elif limitations:
        overall_status = "DEGRADED PERFORMANCE"

    else:
        overall_status = "NORMAL OPERATION"

    return {
        "success": True,
        "simulation": "VaaniSetu Edge Constraint Simulator",

        "input_resources": {
            "available_ram_mb": available_ram_mb,
            "cpu_cores": cpu_cores,
            "network_latency_ms": network_latency_ms,
            "bandwidth_mbps": bandwidth_mbps,
            "internet_available": internet_available
        },

        "resource_assessment": {
            "ram": ram_status,
            "cpu": cpu_status,
            "network_latency": latency_status,
            "network_bandwidth": bandwidth_status,
            "connectivity": connectivity_status
        },

        "overall_status": overall_status,

        "limitations": limitations,

        "recommendations": recommendations,

        "simulation_note": (
            "This is a software-based simulation. "
            "Actual hardware resources and network "
            "conditions are not modified or measured."
        )
    }