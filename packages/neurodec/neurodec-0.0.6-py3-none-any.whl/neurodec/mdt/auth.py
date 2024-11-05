from __future__ import annotations
import appdirs
import os
from hashlib import sha256
import logging
import time
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

# Environment variables where the keys should be located.
_PUBLIC_KEY_ENV = f"ND_MDT_PUBLIC_KEY"
_PRIVATE_KEY_ENV = f"ND_MDT_PRIVATE_KEY"


def get_credentials() -> dict:
    """Load credentials from environment variables or a file.

    API requests need to be authenticated via credentials. To do this, a public and a private key need to be loaded
    first. These two are searched in the following locations, in order:
    - A pair of environment variables named ND_MDT_PUBLIC_KEY and ND_MDT_PRIVATE_KEY.
    - A plain text file in the local user configuration directory. The full file path is platform-specific (all paths
        below correspond to the actual file, not just the path of the directory containing it):
        - Mac OS X: ~/Library/Preferences/neurodec/mdt/credentials
        - Unix: ~/.config/neurodec/mdt/credentials
        - Windows: C:\\Documents and Settings\\<username>\\Application Data\\neurodec\\neurodec\\mdt\\credentials

    If credentials could not be loaded, an exception is raised. Otherwise, the keys are encoded into a dictionary that
    can be sent to the API to verify the identity of a user.

    Returns:
        A dictionary that contains authentication information to be sent to the server.
    """
    return _credentials_from_keys(*_load_keys())


def _credentials_from_keys(public_key: str, private_key: str):
    """Encode the keys so that they can be safely transmitted to the API."""
    token = int(1000 * time.time())
    signature = sha256((private_key + str(token) + public_key).encode()).hexdigest()
    return {
        "public": public_key,
        "token": token,
        "signature": signature,
    }


def _load_keys() -> Tuple[str, str]:
    """Load authentication keys from environment variables or a file.

    If credentials could not be loaded, an exception is raised.

    Returns:
        A tuple containing the public and private keys.
    """
    # Try loading keys from the environment variables.
    keys = _load_keys_from_environment_variables()
    if keys is not None:
        return keys

    # Try loading keys from a file.
    credentials_file = os.path.join(appdirs.user_config_dir("neurodec"), "mdt", "credentials")
    keys = _load_keys_from_file(credentials_file)
    if keys is not None:
        return keys

    # If nothing works, raise an exception.
    raise RuntimeError(f"Failed to locate credentials from default locations. The following locations were considered:"
                       f"\n- The pair of environment variables '{_PUBLIC_KEY_ENV}' and '{_PRIVATE_KEY_ENV}'"
                       f"\n- The file '{credentials_file}'"
                       f"\nPlease, make sure that credentials are made available in one of these locations before "
                       f"performing any request to the server.")


def _load_keys_from_environment_variables() -> Optional[Tuple[str, str]]:
    """Load authentication keys from a pair of environment variables.

    The keys will be looked for in the environment variables ND_MDT_PUBLIC_KEY and ND_MDT_PRIVATE_KEY respectively.

    Returns:
        The keys found in the target environment variables. If any of these is not found, None is returned instead.
    """
    if any(k not in os.environ for k in (_PUBLIC_KEY_ENV, _PRIVATE_KEY_ENV)):
        return None
    return os.environ[_PUBLIC_KEY_ENV], os.environ[_PRIVATE_KEY_ENV]


def _load_keys_from_file(file_name: str) -> Optional[Tuple[str, str]]:
    """Load authentication keys from a given file.

    The first line of the file is used as public key, and the second line as private key. Newline characters are
    stripped from the end of these lines. If the file contains more than two lines, all other lines are ignored.

    Args:
        file_name: Path to a plain text file containing at least two lines.
    Returns:
        A tuple containing the public and private keys found in the given file. If the file does not exist, None is
        returned instead.
    """
    # If the file does not exist, return None.
    if not os.path.isfile(file_name):
        return None

    # The file exists: read its content.
    with open(file_name, "r") as f:
        lines = f.read().splitlines()

    # Make sure that the credentials file is well-structured before returning the keys.
    if len(lines) < 2:
        raise RuntimeError(f"Invalid credentials file '{file_name}'. A well-formatted credentials file should contain "
                           f"at least 2 lines (one for the public key, the other for the private key). The given file "
                           f"contains {len(lines)} lines.")

    return lines[0], lines[1]
