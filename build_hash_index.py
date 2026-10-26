def build_hash_index(values):
    index = MyHashMap()

    for row_id, key in enumerate(values):
        index.put(key, row_id)

    return index
