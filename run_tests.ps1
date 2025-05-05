# Установка переменной PYTHONPATH и запуск pytest
$env:PYTHONPATH = "."
pytest src/convert_code/test.py -v
pytest src/convert_code/test_text.py -v
#pytest src/convert_code/test_video.py -v
pytest src/convert_code/test_archive.py -v
