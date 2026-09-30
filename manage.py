#!/usr/bin/env python3
"""Tiny DRF-shaped contract generator used only for API Analyzer testing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


BASE_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "CodeForge Testing API",
        "version": "1.0.0",
    },
    "paths": {
        "/users": {
            "get": {
                "summary": "List users",
                "operationId": "listUsers",
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/User"
                                    },
                                }
                            }
                        },
                    }
                },
            }
        }
    },
    "components": {
        "schemas": {
            "User": {
                "type": "object",
                "required": ["id", "full_name"],
                "properties": {
                    "id": {"type": "integer"},
                    "full_name": {"type": "string"},
                },
            }
        }
    },
}


def generate_contract(output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(BASE_SPEC, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Generated OpenAPI contract: {path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    spectacular = subparsers.add_parser("spectacular")
    spectacular.add_argument("--file", default="openapi.json")
    spectacular.add_argument("--validate", action="store_true")

    args = parser.parse_args()

    if args.command != "spectacular":
        parser.error("Use: python manage.py spectacular --file openapi.json --validate")

    generate_contract(args.file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
