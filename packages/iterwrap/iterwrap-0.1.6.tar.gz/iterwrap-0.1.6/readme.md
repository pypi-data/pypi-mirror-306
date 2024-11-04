Wrapper on an iterable to support interruption & auto resume, retrying and multiprocessing.

There are three APIs provided:

1. IterateWrapper: wrap some iterables to provide automatic resuming on interruption, no retrying and limited to sequence
2. retry_dec: decorator for retrying a function on exception
3. iterate_wrapper: need hand-crafted function but support retrying, multiprocessing and iterable.

See the source code for usage.
