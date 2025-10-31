import subprocess
from typing import Optional


def getGitRoot() -> Optional[str]:
    """
    Get the git repository root directory.
    
    Returns:
        The absolute path to the git repository root, or None if not in a git repository.
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Not in a git repository or git not available
        return None
