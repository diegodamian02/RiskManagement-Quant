from dataclasses import dataclass

@dataclass
class AppConfig:
    cache_dir: str = "data"
    ewma_lambda: float = 0.94
