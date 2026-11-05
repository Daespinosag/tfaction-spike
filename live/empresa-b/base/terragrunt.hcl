terraform {
  source = "${get_repo_root()}/catalog/modules/demo"
}

inputs = {
  name = "empresa-b-base"
}
# Verify: plan en las 4 units
