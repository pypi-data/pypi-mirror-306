from typing import TypeAlias, Literal, Dict, Optional, Union
from genotype import Model
from .openai import OpenAIProviders
from .anthropic import AnthropicProviders


PackageNpmDependencies : TypeAlias = Dict[str, str]
"""npm package dependencies."""


class PackageNpm(Model):
    """npm package."""

    type: Literal["npm"]
    """Package type."""
    name: str
    """Package name."""
    version: str
    """Package version."""
    shasum: str
    """SHA1 checksum."""
    tarball: str
    """Tarball URL."""
    tag: str
    """Tag name."""
    time: int
    """Unix timestamp in milliseconds."""
    dependencies: PackageNpmDependencies
    """Package dependencies."""


Package : TypeAlias = PackageNpm
"""Collection package."""


class PackageSettingsProviders(Model):
    """Providers map"""

    openai: Optional[OpenAIProviders] = None
    """OpenAI provider."""
    anthropic: Optional[AnthropicProviders] = None
    """Anthropic provider."""


class PackageSettings(Model):
    """Package settings."""

    providers: Optional[PackageSettingsProviders] = None
    """Package providers."""


PackageStatus : TypeAlias = Union[Literal["pending"], Literal["building"], Literal["errored"], Literal["published"]]
"""Status of the package."""


class PackageTrigger(Model):
    """Package trigger message."""

    id: int
    """Package id."""
