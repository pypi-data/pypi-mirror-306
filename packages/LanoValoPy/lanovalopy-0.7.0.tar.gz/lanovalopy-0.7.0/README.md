[discord]: https://discord.gg/wF9JHH55Kp

<div align="center">

[![Downloads](https://static.pepy.tech/badge/lanovalopy)](https://pepy.tech/project/lanovalopy)

</div>

# LanoValoPy (Lanore Valorant Python)

LanoValoPy is a python-based wrapper for the following Valorant Rest API:

https://github.com/Henrik-3/unofficial-valorant-api

This API is free and freely accessible for everyone. An API key is optional but not mandatory. This project is NOT being worked on regularly.

This is the first version. There could be some bugs, unexpected exceptions or similar. Please report bugs on our [discord].

### API key

You can request an API key on [Henrik's discord server](https://discord.com/invite/X3GaVkX2YN) <br> It is NOT required to use an API key though!

## Summary

1. [Introduction](#introduction)
2. [Download](#download)
3. [Documentation](#documentation)
4. [Support](#support)

## Introduction

Some requests may take longer.

### Get Account and mmr informations

```python
import asyncio
from lano_valo_py import LanoValoPy
from lano_valo_py.valo_types.valo_enums import MMRVersions, Regions

async def main():
    # Initialize the API client with your token
    api_client = LanoValoPy(token="YOUR_TOKEN_HERE")

    # Example: Get Account Information
    account_options = AccountFetchOptionsModel(name="LANORE", tag="evil")
    account_response = await api_client.get_account(account_options)
    print(account_response)

    # Example: Get MMR
    mmr_options = GetMMRFetchOptionsModel(
        version=MMRVersions.v2,
        region=Regions.eu,
        name="Lanore",
        tag="evil",
    )
    mmr_response = await api_client.get_mmr(mmr_options)
    print(mmr_response)


if __name__ == "__main__":
    asyncio.run(main())

```

## Download

``` bash
pip install lanovalopy@latest

```

## Documentation

The detailed documentations are still in progress.

## Support

For support visit my [discord] server