# BFloat.ai Python SDK

[![PyPI version](https://img.shields.io/pypi/v/bfloat.svg)](https://pypi.org/project/bfloat/)
[![Python](https://img.shields.io/pypi/pyversions/bfloat.svg)](https://www.python.org/)
[![Async Support](https://img.shields.io/badge/async-ready-green.svg)](https://docs.python.org/3/library/asyncio.html)

A powerful and intuitive Python SDK for interacting with the bfloat.ai API. Manage browser automation sessions with ease using modern async/await patterns.

## Features

- 🚀 Full type hinting support with dataclasses
- 💪 Async/await support using aiohttp
- 🛡️ Robust error handling
- 🔄 Complete session lifecycle management
- ⚙️ Flexible browser configuration
- 📘 Extensive documentation and examples

## Installation

```bash
# Using pip
pip install bfloat

# Using poetry
poetry add bfloat

# Using pipenv
pipenv install bfloat
```

## Quick Start

```python
from bfloat import BfloatSDK, DEFAULT_BROWSER_CONFIG
import asyncio

# Initialize the SDK
bfloat = BfloatSDK('your-api-key')

# Create and manage a session
async def example():
    try:
        # Create a new session
        session = await bfloat.create_session({
            'browser': DEFAULT_BROWSER_CONFIG,
            'lifetime': 3600,
            'keep_alive': True
        })

        print(f'Session created: {session.id}')
        print(f'Debug URL: {session.debug_info.ws_debugger_url}')

        # Stop the session when done
        await bfloat.stop_session(session.id)
    except Exception as error:
        print(f'Error: {error}')
    finally:
        await bfloat.close()

# Run the example
asyncio.run(example())
```

## API Reference

### Initialization

```python
bfloat = BfloatSDK(api_key: str, base_url: str = "https://api.bfloat.ai/v1")
```

### Methods

#### List Sessions
```python
sessions = await bfloat.list_sessions()
```

#### Get Session Details
```python
session = await bfloat.get_session(session_id: str)
```

#### Create Session
```python
session = await bfloat.create_session(config: SessionConfig)
```

#### Stop Session
```python
result = await bfloat.stop_session(session_id: str)
```

### Configuration

#### Browser Configuration
```python
@dataclass
class BrowserConfig:
    type: str
    settings: Optional[BrowserSettings] = None
    block_ads: Optional[bool] = None
    proxy: Optional[bool] = None

@dataclass
class BrowserSettings:
    os: Optional[List[str]] = None
    devices: Optional[List[str]] = None
    screen: Optional[Dict[str, int]] = None
    locales: Optional[List[str]] = None
```

#### Session Configuration
```python
@dataclass
class SessionConfig:
    browser: BrowserConfig
    lifetime: Optional[int] = None
    keep_alive: Optional[bool] = None
```

## Error Handling

The SDK provides a custom `BFloatError` class for error handling:

```python
try:
    session = await bfloat.create_session(config)
except BFloatError as error:
    print(f'Status: {error.status}')
    print(f'Message: {error.message}')
    print(f'Response: {error.response}')
```

## Complete Example

```python
from bfloat import BfloatSDK, BFloatError, DEFAULT_BROWSER_CONFIG, SessionConfig
import asyncio

async def run_browser_session():
    bfloat = BfloatSDK('your-api-key')

    try:
        # List existing sessions
        sessions = await bfloat.list_sessions()
        print(f'Active sessions: {len(sessions)}')

        # Create a new session
        config = SessionConfig(
            browser=DEFAULT_BROWSER_CONFIG,
            lifetime=3600
        )
        session = await bfloat.create_session(config)

        print(f'New session: {session.id}')
        print(f'Debug URL: {session.debug_info.ws_debugger_url}')

        # Get session details
        details = await bfloat.get_session(session.id)
        print(f'Session status: {details.status}')

        # Stop session
        await bfloat.stop_session(session.id)
        print('Session stopped successfully')

    except BFloatError as error:
        print(f'BFloat API error: {error}')
        print(f'Status: {error.status}')
    except Exception as error:
        print(f'Unexpected error: {error}')
    finally:
        await bfloat.close()

# Run the example
if __name__ == "__main__":
    asyncio.run(run_browser_session())
```

## Development

```bash
# Install dependencies
poetry install

# Run tests
pytest

# Build
poetry build

# Generate documentation
pdoc --html bfloat_sdk
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: [https://docs.bfloat.ai](https://docs.bfloat.ai)
- Issues: [GitHub Issues](https://github.com/bfloat-inc/python-sdk-python/issues)
- Email: support@bfloat.ai

## Security

If you discover a security vulnerability, please send an email to security@bfloat.ai. All security vulnerabilities will be promptly addressed.
