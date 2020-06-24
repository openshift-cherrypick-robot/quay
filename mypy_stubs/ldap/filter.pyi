from ldap.functions import strf_secs as strf_secs
from typing import Any, Optional

def escape_filter_chars(assertion_value: Any, escape_mode: int = ...): ...
def filter_format(filter_template: Any, assertion_values: Any): ...
def time_span_filter(filterstr: str = ..., from_timestamp: int = ..., until_timestamp: Optional[Any] = ..., delta_attr: str = ...): ...
