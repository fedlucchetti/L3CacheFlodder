# L3CacheFlodder

## Description
- Source files necessary to replicate experimental results.
- Cache floods and flushed L3 on all cores 
- Monitors Execution times

## Running
- Build Apollo module [Inside docker]
`./apollo build_opt_gpu control`

- Run Control task
`cyber_launch start /modules/control/launch/control.launch`

- Flood L3 cache on all cores [Outside Docker]
`g++ cache_flodder.c -o cache_flodder`
`python cahce_flodder.py`
