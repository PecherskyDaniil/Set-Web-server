Для развертывания данного червера вам понадобится:
1. Установить Python на сервер:
` sudo apt install python3-pip `
2.  Установить Flask на сервер:
` pip3 install Flask `
3.  Установить Gunicorn:
 ` sudo apt install gunicorn `
4.  Установите nginx:
` sudo apt install nginx `
5.   Перенесите файлы с репозитория в отдельную папку (далее будет указываться как setapp, но вы можете назвать по своему, главное не забудьте поменять это названия в конфигах и командах)
6.   В папке с файлами пропишите эту команду
` export FLASK_APP=hello `
7.   В config файле вашего сайта, в разделе location укажите в директиве proxy_pass путь к вашему сокету (имя юзера и setapp ваши):
` location / {
        proxy_pass http://unix:/home/user/setapp/setapp.sock;
    }
`
8.     Чтобы создать собственный сервис, создайте файл в папке /etc/systemd/system. Содержание файла setapp.service ниже.После создания перезагрузите системного демона командой `systemctl daemon-reload `

`[Unit]
Description=setapp.service - A Flask application run with Gunicorn.
After=network.target

[Service]
User=user
Group=user
WorkingDirectory=/home/user/setapp
ExecStart=/usr/bin/gunicorn --workers 3 \
--bind unix:/home/user/setapp/setapp.sock wsgi:app

[Install]
WantedBy=multi-user.target
`
9. После запустите сервис командой `sudo service setapp start `
С этого момента публичный адрес вашей виртуальной машины должен отвечать на запросы. Больше о доступных запросах по ссылке https://github.com/Krushiler/com.krushiler.set-game-server/blob/master/Readme.md
