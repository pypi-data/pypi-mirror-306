# a360-python-libraries

Python shared libraries for a360 applications

## License
This software is proprietary and is intended solely for use by Aesthetics-360 Inc.. Unauthorized use, distribution, or modification of this software outside of Aesthetics-360 Inc. is strictly prohibited.

## Add package into your project

```bash
poetry add a360-python-libraries
```

## Usage

### Role based access control

```python
from fastapi import APIRouter, Depends

from a360_security.depends import require_role
from a360_security.enums import Role

router = APIRouter()

@router.get(
    ...,
    dependencies=[Depends(require_role(Role.ADMIN))]
)
def get() -> dict:
    ...
```

You can provide multiple roles to the `require_role` dependency, and they will be checked in OR fashion.

```python
from fastapi import APIRouter, Depends

from a360_security.depends import require_role
from a360_security.enums import Role

router = APIRouter()

@router.get(
    ...,
    dependencies=[Depends(require_role(Role.ADMIN, Role.SERVICE))]
)
def get() -> dict:
    ...
```


### User valid practice dependency

```python
from fastapi import APIRouter, Depends

from a360_security.depends import valid_practice

router = APIRouter()

@router.get(
    ...,
    dependencies=[Depends(valid_practice())]
)
def get() -> dict:
    ...
```


### User dependency

```python
from fastapi import APIRouter, Depends

from a360_security.depends import require_user
from a360_security.dto import UserDTO

router = APIRouter()

@router.get(
    ...,
)
def get(user: UserDTO = Depends(require_user)) -> dict:
    ...
```


### Client platform

```python
from fastapi import APIRouter, Depends

from a360_security.depends import require_client_platform
from a360_security.enums import ClientPlatform

router = APIRouter()

@router.get(
    ...,
)
def get(client_platform: ClientPlatform = Depends(require_client_platform)) -> dict:
    ...
```

### Internal services

```python
from fastapi import APIRouter, Depends

from a360_services import get_dictionary_service
from a360_services.services import DictionaryService

router = APIRouter()

@router.get(
    ...,
)
def get(dict_service: DictionaryService = Depends(get_dictionary_service)) -> dict:
    medical_conditions = dict_service.get_medical_conditions()
```

### Email notification

```python
from fastapi import APIRouter, Depends

from a360_notification import get_mail_service
from a360_notification.services import AWSSesService

router = APIRouter()

@router.post(
    ...,
)
def create(mail_service: AWSSesService = Depends(get_mail_service)):
    mail_service.send_email(
        recipient_name='John Doe',
        recipient_address='john.doe@example.com',
        subject='Test email',
        html_content='<h1>Test email</h1>',
    )
```