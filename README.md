# RSA Crypter

## Описание
Программа для шифрования и расшифровывания файлов с визуальным интерфейсом

**Версия 1.2**

![](https://github.com/Raidzin/rsa_crypter/blob/main/design_example.png?raw=true)

## Используется

- python 3.7
- PyQt5
- pyinstaller

## Запуск

- ### Скачать репозиторий
  ```shell
  git clone https://github.com/Raidzin/rsa_crypter.git
  ```
  
- ### Перейти в директорию rsa_crypter
  ```shell
  cd rsa_crypter
  ```
- ### Создать виртуальное окружение
  ```shell
  python -m venv venv
  ```

- ### Активировать виртуальное окружение
  - #### Для Linux и MacOS
    ```shell
    source venv/bin/activate
    ```
  - #### Для Windows
    ```commandline
    venv\Scripts\activate.bat
    ```

- ### Установить зависимости (в виртуальном окружении)
  ```shell
  pip install -r requirements.txt
  ```

- ### Запустить программу (в виртуальном окружении)
  ```shell
  python crypter.py
  ```
  
## Установка

Если есть желание/необходимость создать исполняемый файл в проекте есть pyinstaller

- ### Проверка работы pyinstaller (в виртуальном окружении)
  ```shell
  pyinstaller --version
  ```
  если версия вывелась - всё работает без проблем,

  если не вывелась - нужно решать проблему индивидуально

- ### Создание исполняемого файла: (в виртуальном окружении)
  ```shell
  pyinstaller --onefile --icon=icon.ico --noconsole crypter.py
  ```
  #### исполняемый файл будет создан в папке `dist`
  
## Разработчик

- [RAIDZIN](https://github.com/Raidzin "github.com/Raidzin")