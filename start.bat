@echo off
start "MusicPlayer" /D "C:\projects\MusicPlayerBackend2" "C:\Python27\pythonw.exe" manage.py runserver ^
--noreload --settings MusicPlayerBackend2.local_settings
