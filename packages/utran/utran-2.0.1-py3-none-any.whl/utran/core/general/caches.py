from typing import Optional as _Optional

from cachetools import LRUCache, TTLCache, LFUCache, FIFOCache, RRCache, TLRUCache
CacheType = _Optional[LRUCache | TTLCache | LFUCache | FIFOCache | RRCache | TLRUCache]
