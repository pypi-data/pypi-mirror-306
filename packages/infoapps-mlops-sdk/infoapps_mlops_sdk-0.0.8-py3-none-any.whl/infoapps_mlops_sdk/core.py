from .tracking.experiment import HubExperiment, TensorboardExperiment, PytorchLightningExperiment, MLFlowExperiment

class PlatformType:
    HUB = "turihub"
    # NEPTUNE = "neptune"
    TENSORBOARD = "tensorboard"
    PYTORCH_LIGHTNING = "pytorch_lightning"
    MLFLOW = "mlflow"

def initialize_experiment(platform_type, **kwargs):
    if platform_type == PlatformType.HUB:
        return HubExperiment(**kwargs)
    elif platform_type == PlatformType.TENSORBOARD:
        return TensorboardExperiment(**kwargs)
    elif platform_type == PlatformType.PYTORCH_LIGHTNING:
        return PytorchLightningExperiment(**kwargs)
    elif platform_type == PlatformType.MLFLOW:
        return MLFlowExperiment(**kwargs)
    else:
        raise ValueError(f"Unsupported platform type: {platform_type}")
