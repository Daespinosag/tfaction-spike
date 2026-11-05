terraform {
  source = "${get_repo_root()}/catalog/modules/demo"
}

inputs = {
  name = "empresa-a-base"
}
# PC: empresa-a/base (C)
# R4: dos empresas (con capa)
