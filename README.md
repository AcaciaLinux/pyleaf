# Pyleaf
Pyleaf is a wrapper for the leaf package manager. It uses the cleaf wrapper to implement the leaf functionality for python.

# config
To use the leaf config, for example to enable the 'NoAsk' flag, just refer the following snippet:
```python
leafcore = Leafcore()
leafcore.setBoolConfig(LeafConfig_bool.CONFIG_NOASK, True)
```
