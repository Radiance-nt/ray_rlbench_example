import gymnasium as gym
from gymnasium import spaces
from rlbench.action_modes.action_mode import MoveArmThenGripper
from rlbench.action_modes.arm_action_modes import JointPosition, JointVelocity
from rlbench.environment import Environment
from rlbench.observation_config import ObservationConfig
from rlbench.tasks import ReachTarget as task_nn
from rlbench.action_modes.gripper_action_modes import Discrete
import numpy as np


class RLBenchEnv(gym.Env):

    def __init__(self):
        self.episode_length = 300
        self.ts = 0
        self.num_error = 0
        obs_config = ObservationConfig(
            joint_velocities=False,
            joint_positions=True,
            joint_forces=False,
            gripper_open=False,
            gripper_pose=False,
            task_low_dim_state=True,
        )
        obs_config.set_all_high_dim(False)
        action_mode = MoveArmThenGripper(
            arm_action_mode=JointVelocity(),
            gripper_action_mode=Discrete()
        )
        self.env = Environment(
            action_mode, obs_config=obs_config, headless=True
        )
        self.env.launch()
        self.task = self.env.get_task(task_nn)
        _, obs = self.task.reset()
        self.action_space = spaces.Box(
            low=-1.0, high=1.0, shape=self.env.action_shape)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=obs.get_low_dim_data().shape)

    def action_input(self, action):
        action = action * 0.05
        return action

    def _extract_obs(self, obs):
        return obs.get_low_dim_data()

    def reset(self, seed=None, options={}):
        descriptions, obs = self.task.reset()
        self.ts = 1
        return self._extract_obs(obs), {}

    def step(self, action):
        action = self.action_input(action)
        obs, reward, done = self.task.step(action)
        if reward == 10:
            print('========success=========')
            reward = 10
        self.ts = self.ts + 1
        if self.ts > self.episode_length:
            return self._extract_obs(obs), reward, True, True, {},
        else:
            return self._extract_obs(obs), reward, done, False, {}

    def close(self):
        self.env.shutdown()

