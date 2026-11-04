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
  name = "empresa-a-app-v2"
  dep  = dependency.base.outputs.id
}
