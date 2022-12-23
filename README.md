# wapp_file_manager

Файловый менеджер на flask. 

- Есть просмотр изображений
- Подсветка кода тестовых файлов
- Есть просмотр PDF
- Есть просмотр DJVU с конвертацией в PDF
- Все в одном файле. Может запускать из архива (zipapps)

![](screenshots/2022-12-17_18-16.png)

## Запуск

```bash
wget https://github.com/hightemp/wapp_file_manager/releases/latest/download/wapp_file_manager.pyz
chmod a+x ./wapp_file_manager.pyz
./wapp_file_manager.pyz
```

## Упаковка

```bash
# https://docs.python.org/3/library/zipapp.html
python3 -m zipapp wapp_file_manager -p "/usr/bin/env python3"
```

## Зависимости

- apt пакеты
    - djvulibre-bin
    - unoconv