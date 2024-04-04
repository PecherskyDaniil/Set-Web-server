
Для развертывания данного сервера вам понадобится:


#. Установить Python на сервер:
   ``sudo apt install python3-pip``
#. Установить Flask на сервер:
   ``pip3 install Flask``
#. Установить Gunicorn:
   ``sudo apt install gunicorn``
#. Установите nginx:
   ``sudo apt install nginx``
#. Перенесите файлы с репозитория в отдельную папку (далее будет указываться как setapp, но вы можете назвать по своему, главное не забудьте поменять это названия в конфигах и командах)
#. В папке с файлами пропишите эту команду
   ``export FLASK_APP=hello``
#. 
   В config файле вашего сайта, в разделе location укажите в директиве proxy_pass путь к вашему сокету (имя юзера и setapp ваши):

   .. code-block::

      location / {
         proxy_pass http://unix:/home/user/setapp/setapp.sock;

      }

#. Чтобы создать собственный сервис, создайте файл в папке /etc/systemd/system. Содержание файла setapp.service ниже.После создания перезагрузите системного демона командой
   ``systemctl daemon-reload``

.. code-block::

   [Unit]
   Description=setapp.service - A Flask application run with Gunicorn.
   After=network.target

   [Service]
   User=user
   Group=user
   WorkingDirectory=/home/user/setapp
   ExecStart=/usr/bin/gunicorn --workers 3 --bind unix:/home/user/setapp/setapp.sock wsgi:app

   [Install]
   WantedBy=multi-user.target


#. После запустите сервис командой ``sudo service setapp start``
   С этого момента публичный адрес вашей виртуальной машины должен отвечать на запросы. Больше о доступных запросах по ссылке https://github.com/Krushiler/com.krushiler.set-game-server/blob/master/Readme.md
