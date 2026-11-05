variable "name" {
  type = string
}

variable "dep" {
  type    = string
  default = ""
}

resource "terraform_data" "this" {
  input = "${var.name}:${var.dep}"
}

output "id" {
  value = terraform_data.this.id
}
# R2: modulo compartido (con capa)
