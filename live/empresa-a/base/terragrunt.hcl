terraform {
  source = "${get_repo_root()}/catalog/modules/demo"
}

inputs = {
  name = "empresa-a-base"
}
# Verify: plan en las 4 units
