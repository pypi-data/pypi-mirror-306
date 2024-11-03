![Edgeberry Banner](https://raw.githubusercontent.com/Edgeberry/.github/main/brand/Edgeberry_banner_SDK.png)

<img src="https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/community/logos/python-logo-only.png" align="right" width="10%"/>

The **Edgeberry Python SDK** is a software library to facilitate communication between Python application and the **Edgeberry Device Software**. The Edgeberry Python SDK interacts with the Edgeberry Device Software throught the D-Bus API.

<br clear="right"/>

## Usage
Install the package using `pip`
```sh
pip install edgeberry
```
Import the library in your application
```python
from edgeberry import Edgeberry
edgeberry = Edgeberry()
```
Available methods
```python
edgeberry.set_status("level", "message")
edgeberry.set_application_info("name", "version", "description")
```

## License & Collaboration
**Copyright© 2024 Sanne 'SpuQ' Santens**. The Edgeberry Device Software is licensed under the **MIT License**. The [Rules & Guidelines](https://github.com/Edgeberry/.github/blob/main/brand/Edgeberry_Trademark_Rules_and_Guidelines.md) apply to the usage of the Edgeberry™ brand.

### Collaboration

If you'd like to contribute to this project, please follow these guidelines:
1. Fork the repository and create your branch from `main`.
2. Make your changes and ensure they adhere to the project's coding style and conventions.
3. Test your changes thoroughly.
4. Ensure your commits are descriptive and well-documented.
5. Open a pull request, describing the changes you've made and the problem or feature they address.