"""Errors raised while loading and validating the dataset."""


class DatasetValidationError(Exception):
    """A dataset YAML file does not conform to SCHEMA.md."""

    def __init__(self, path, issues):
        self.path = path
        self.issues = issues
        message = f"{path}: " + "; ".join(issues)
        super().__init__(message)
