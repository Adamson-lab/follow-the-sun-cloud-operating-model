package enterprise.operations.followthesun

default allow_pod_dispatch = false

allow_pod_dispatch if {
    input.enclave == "commercial-global"
}

allow_pod_dispatch if {
    input.enclave == "fedramp-high-us"
    startswith(input.target_pod, "AMER-SOVEREIGN")
}
