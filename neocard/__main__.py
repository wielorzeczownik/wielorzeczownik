import sys
from urllib.error import URLError

from .cli import main

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(130)
    except (OSError, URLError, ValueError, KeyError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
