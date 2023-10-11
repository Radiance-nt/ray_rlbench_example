# RLBench_on_Ray

1. Insatll CoppeliaSim, PyRep
2. Insatll RLBench
3. Install Ray
4. Run main.py

```bash
export COPPELIASIM_ROOT=~/Dependency/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$COPPELIASIM_ROOT
export QT_QPA_PLATFORM_PLUGIN_PATH=$COPPELIASIM_ROOT
xvfb-run -a python main.py 
```


```python
import os

os.environ['COPPELIASIM_ROOT'] = '/home/radiance/Dependency/CoppeliaSim_Edu_V4_1_0_Ubuntu20_04'
if 'LD_LIBRARY_PATH' in os.environ:
    os.environ['LD_LIBRARY_PATH'] += ':' + os.environ['COPPELIASIM_ROOT']
else:
    os.environ['LD_LIBRARY_PATH'] = os.environ['COPPELIASIM_ROOT']
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.environ['COPPELIASIM_ROOT']

```