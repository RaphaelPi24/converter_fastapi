# Установка переменной PYTHONPATH и запуск pytest
# $env:PYTHONPATH = "."
pytest src/convert_code/test_text_func.py -v
pytest src/convert_code/test_text_interface.py -v
pytest src/convert_code/test_video_interface.py -v
pytest src/convert_code/test_archive_interface.py -v
pytest src/convert_code/test_image_func.py -v
pytest src/convert_code/test_image_interface.py -v

