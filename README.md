# tfaction-spike

Spike de orquestación de IaC: [tfaction](https://github.com/suzuki-shunsuke/tfaction) v2.3.4 (fork espejo `daespinosag/tfaction`, sin cambios de código, referenciado por SHA) con Terragrunt 1.1.6 y OpenTofu 1.13.2 (instalados con aqua, ver `aqua.yaml`).

- Datos ficticios; solo `terraform_data`. Ningún provider de nube.
- Backend local: el state no persiste entre jobs. El spike mide orquestación, no state.
- Units: `live/empresa-{a,b}/{base,app}`; `empresa-a/app` depende de `empresa-a/base`. Módulo compartido: `catalog/modules/demo`.

## Sincronizar el fork

Solo fast-forward: `gh repo sync daespinosag/tfaction` (o `git fetch upstream` y `git merge --ff-only`). Nunca commits propios en el fork; tras sincronizar, actualiza el SHA en los workflows.
