import os

CONVERTED_FOLDER = "converted"
os.makedirs(CONVERTED_FOLDER, exist_ok=True)




def convert_file_to_lowercase(input_path: str, output):
    with open(input_path, 'r', encoding='utf-8') as infile:
        content = infile.read()

    lower_content = content.lower()
    print(f'а сейчас запишем файл uploads/{output} с контентом {lower_content}')
    with open(f'uploads/{output}', 'w', encoding='utf-8') as outfile:
        outfile.write(lower_content)
    print('записано')
def count_characters_in_file(file_path='t1.txt') -> int:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return len(content)

def from_number_to_sec(number):
    return number / 10

