# cololog

`cololog` — это библиотека для логирования с цветным выводом в консоль и возможностью записи логов в файл. Она поддерживает кастомные уровни логирования и цветовую настройку.

## Установка

```bash
pip install cololog
```

## Пример использования

```python
from cololog import cololog

logger = cololog(__name__)
logger.debug("This is a debug message")
```
