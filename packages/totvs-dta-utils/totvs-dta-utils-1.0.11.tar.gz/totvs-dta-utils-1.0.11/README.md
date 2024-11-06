# Dta Utils
=======

**Agilize a integração entre serviços DTA**


### O que são Seriços DTA?

Uma coleção de serviços para facilitar e acelerar o desenvolvimento e monitoramento de Aplicações, com foco em aplicativos de IA generativa.


## Introdução

Esse pacote possui módulos extras que auxiliam o desenvolvimento de integrações com os serviços do DTA.

## Extra "Secrets"

### Instalação

Instale o módulo `secrets` com:
```shell
pip install "totvs-dta-utils[secrets]"
```

Ou utilizando `poetry`:
```shell
poetry add "totvs-dta-utils[secrets]"
```

### Configuração inicial:

Adicione as seguintes variavei ao `.env` do seu projeto:
```env
DTA_ENVIRONMENT="development"
DTA_SECRET_URL="{DTA_SECRET_URL}"
```
> NOTE: Para ambiente em cloud,aonde terá acesso irrestrito aos secrets, o valor do `DTA_ENVIRONMENT`deve ser `production`.

### Utilização

```python
from dta_utils_python import DtaSecrets

auth = DTA_JWT  # CLIENT AUTHORIZATION

secrets = DtaSecrets(authorization=auth,
                     project="dta-empodera")

all_secrets = secrets.all()  # Get the latest version of all secrets
my_secret = secrets.get("MY_SECRET")  # Get the latest version of a secret
my_secret_v2 = secrets.get("MY_SECRET", version=2)  # Get a specific version of a secret
```
> NOTE: For cloud environemnt, no auth is required.

### Demais configurações:
```python
DtaSecrets(
    authorization=auth,
    project="dta-empodera",
    raise_exception: bool = True,  # Default "False" - Raises exception in case of secret retrieving error
    autoload: bool = False,  # Default "True" - Pre loads all project secrets during the Class initialization and keep it on memory caching
)
```

### Tipos de retorno:
- `.get("SECRET_2")`:
```json
dict: {
    "value": "321654"
}
```
> NOTE: retorna None no caso da secret não existir

- `.all()`:
```json
dict: {
    "SECRET_1": "123456",
    "SECRET_2": "321654",
    "SECRET_3": "My secret",
}
```
