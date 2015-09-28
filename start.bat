@echo off
start "MusicPlayer" /D "C:\projects\MusicPlayerBackend2" "C:\Python27\pythonw.exe" manage.py runserver --settings MusicPlayerBackend2.local_settings --noreload 8008
