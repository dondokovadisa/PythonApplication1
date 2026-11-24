# Инструмент визуализации графа зависимостей (Вариант 7)

## Описание
CLI-приложение на Python для построения и визуализации графа зависимостей пакетов pip. 
Работает без использования сторонних менеджеров пакетов (pip, pipdeptree) — данные получаются напрямую через PyPI JSON API.

## Запуск
```bash
./run.sh --package requests --repo https://pypi.org --mode online --output requests.svg --depth 2 --ascii
