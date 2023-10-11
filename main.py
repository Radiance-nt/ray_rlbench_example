import ray
import pyrep.backend.sim
from ray import tune
from ray.tune.registry import register_env
from ray.rllib.models import ModelCatalog
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.rllib.models.torch.fcnet import FullyConnectedNetwork as TorchFC

import torch.nn as nn

from rlbench_custom_env import RLBenchEnv


class TorchCustomModel(TorchModelV2, nn.Module):

    def __init__(self, obs_space, action_space, num_outputs, model_config, name):
        TorchModelV2.__init__(self, obs_space, action_space, num_outputs, model_config, name)
        nn.Module.__init__(self)
        self.fclayer = nn.Sequential(
            nn.Linear(13, 128),
            nn.ReLU(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
        )

    def forward(self, input_dict, state, seq_lens):
        obs = input_dict["obs"]
        out = self.fclayer(obs)
        return out, []


if __name__ == '__main__':
    ray.init(num_gpus=1)

    register_env('RLBenchEnv', lambda _: RLBenchEnv())

    from ray.rllib.algorithms.ppo import PPOConfig

    config = PPOConfig().environment(env="RLBenchEnv").training(train_batch_size=4000)

    tune.run("PPO", config=config)
    ModelCatalog.register_custom_model(
        "my_custom_model", TorchCustomModel
    )

