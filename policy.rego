package kubernetes.admission

# Ensure that containers in a Deployment run as non-root
deny[msg] {
  input.kind == "Deployment"
  some i
  container := input.spec.template.spec.containers[i]
  not container.securityContext.runAsNonRoot == true
  msg = sprintf("Container %s in Deployment %s must not run as root - use runAsNonRoot within container security context", [container.name, input.metadata.name])
}