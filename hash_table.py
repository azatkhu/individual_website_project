class MyHashMap:
    MAX_LOAD_FACTOR = 0.75

    def __init__(self, capacity: int = 8) -> None:
        """Конструктор класса.

        Args:
            capacity: вместимость.
        """

        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def _index(self, key: str | int = None) -> int:
        """
        Возвращает номер bucket для key.

        Args:
            key: ключ.
        
        Returns:
            номер bucket для key.
        """

        return hash(key) % self.capacity

    def load_factor(self) -> float:
        """Возвращает текущий коэффициент заполнения.
        
        Returns:
            текущий коэффициент заполнения.
        """

        return self.size / self.capacity

    def _resize(self) -> None:
        """Меняет размер структуры."""

        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]

        for bucket in old_buckets:
          for key, value in bucket:

            index = self._index(key)
            self.buckets[index].append((key, value))

    def put(self, key: int | str = None, value: int | str = 0) -> None:
        """Добавление ключа и значения.
        
        Args: 
            key: ключ.
            value: значение.
        """

        index = self._index(key)
        bucket = self.buckets[index]

        for i in range(len(bucket)):
          if key == bucket[i][0]:
            bucket[i] = (key, value)

            return

        if (self.size + 1) / self.capacity > self.MAX_LOAD_FACTOR:
          self._resize()
          index = self._index(key)

        self.buckets[index].append((key, value))
        self.size += 1

    def get(self, key: int | str) -> int | str | None:
        """Получение значения по ключу.
        
        Args: 
            key: ключ.
        
        Returns: 
            prev_value: значение, если ключ есть, None, если не нашлось.
        """

        index = self._index(key)
        bucket = self.buckets[index]

        for prev_key, prev_value in bucket:
          if prev_key == key:

            return prev_value

        return None

    def contains(self, key: int | str = None) -> bool:
        """Проверка по ключу, существует ли элемент.

        Args:
            key: ключ.
        """

        index = self._index(key)
        bucket = self.buckets[index]

        for prev_key, prev_value in bucket:
          if prev_key == key:
            return True

        return False

    def remove(self, key: int | str = None) -> bool:
        """Убрать значение по ключу.
        
        Args: 
            key: ключ.
        
        Returns: 
            True: если удалили.
            False: если ключа не было.
        """

        index = self._index(key)
        bucket = self.buckets[index]

        for i in range(len(bucket)):
          if key == bucket[i][0]:
            bucket.pop(i)
            self.size -= 1

            return True

        return False

    def __len__(self) -> int:
        """Возвращает размер структуры, то есть количество пар ключ-значение."""
        
        return self.size
