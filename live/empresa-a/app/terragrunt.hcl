terraform {
  source = "${get_repo_root()}/catalog/modules/demo"
}

dependency "base" {
  config_path = "../base"

  mock_outputs = {
    id = "mock-base-id"
  }
  mock_outputs_allowed_terraform_commands = ["init", "validate", "plan", "providers", "show"]
}

inputs = {
  name = "empresa-a-app"
  dep  = dependency.base.outputs.id
}
# Verify: plan en las 4 units
