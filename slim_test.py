import math
import os
import numpy as np
import tensorflow as tf

import model as model_env
import agent
import architecture as policies
import poke_environ as env

# SubprocVecEnv creates a vector of n environments to run them simultaneously.
from baselines.common.vec_env.subproc_vec_env import SubprocVecEnv
from baselines.common.vec_env.dummy_vec_env import DummyVecEnv
from tensorflow.keras import backend as K

def get_model(policy, env, nsteps, total_timesteps, gamma, lam, vf_coef, ent_coef, lr, cliprange, max_grad_norm, log_interval):
	noptepochs = 4
	nminibatches = 8

	if isinstance(lr, float): lr = constfn(lr)
	else: assert callable(lr)
	if isinstance(cliprange, float): cliprange = constfn(cliprange)
	else: assert callable(cliprange)

	# Get the nb of env
	nenvs = env.num_envs

	# Get state_space and action_space
	ob_space = env.observation_space
	ac_space = env.action_space

	#Calculate the batch size
	batch_size = nenvs * nsteps # For instance if we take 5 steps and we have 5 environments batch_size = 25

	batch_train_size = batch_size // nminibatches

	assert batch_size % nminibatches == 0

	#Instantiate the model object (that creates step_model and train_model)
	model = model_env.Model(policy=policy, ob_space=ob_space, action_space=ac_space,nenvs=nenvs, nsteps=nsteps,
		ent_coef=ent_coef,vf_coef=vf_coef,max_grad_norm=max_grad_norm)
	return model

def main():
  load_path = './models/20/model.ckpt'
  config = tf.ConfigProto()

  # Avoid warning message errors
  os.environ['CUDA_VISIBLE_DEVICES'] = '0'

  # Allowing GPU memory growth
  config.gpu_options.allow_growth = True
  K.clear_session()
  with tf.Session(config=config):

      model = get_model(policy=policies.PPOPolicy,
                                  env=SubprocVecEnv([
                                          env.make_poke_env(),
                                          env.make_poke_env(),
                                          env.make_poke_env(),
                                          env.make_poke_env(),
                                          env.make_poke_env(),
                                          env.make_poke_env(),
                                          env.make_poke_env(),
                                          env.make_poke_env(),
                                          env.make_poke_env(),
                                          env.make_poke_env(),
                                          env.make_poke_env(),
                                          env.make_poke_env(),
                                          env.make_poke_env(),
                                          env.make_poke_env(),
                                          env.make_poke_env(),
                                          env.make_poke_env(),
                                      ]),
                                  nsteps=32, # Steps per environment
      #							nsteps=2048, # Steps per environment
      #							total_timesteps=10000000,
                                  total_timesteps=10000000,
                                  gamma=0.99,
                                  lam=0.95,
                                  vf_coef=0.5,
                                  ent_coef=0.01,
                                  lr = lambda _:2e-4,
                                  cliprange = lambda _:0.2, # 0.1 * learning_rate
                                  max_grad_norm = 0.5,
                                  log_interval  = 10)
      model.load(load_path)
      
      print(model_env.testing(model))

if __name__ == '__main__':
	main()
