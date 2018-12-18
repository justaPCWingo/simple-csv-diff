try:
    from . import csvDiff
except ImportError:
    import csvDiff

csvDiff.runcCsvDiff()
