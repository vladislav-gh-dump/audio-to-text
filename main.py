import pathlib
import os
import whisper


def cut_dir(_dir: str = ""):
    __dir = _dir
    if len(__dir) >= 1 and (__dir[-1] == "\\" or __dir[-1] == "/"):
        __dir = __dir[:-1]

    return __dir


def get_input_files(exts: list = None, _dir: str = f"{os.getcwd()}\\input"):
    if exts is None:
        exts = ["*.mp3"]

    path_to_input_dir = cut_dir(_dir)
    input_files = []

    for ext in exts:
        input_files.extend(pathlib.Path(path_to_input_dir).glob(f"{ext}"))

    return input_files


def edit_text(text: str, lines_break: bool = True, count_words_in_line: int = 5):
    new_text = text
    if lines_break:
        list_words = new_text.split()
        list_words.insert(0, '')
        new_text = ''

        if count_words_in_line <= 0:
            count_words_in_line = 5

        for i in range(1, len(list_words)):
            list_words[i] = f"{list_words[i]} "
            if i % count_words_in_line == 0:
                list_words[i] = f"{list_words[i]}\n"
            new_text += list_words[i]

    return new_text


def write_txt_file(text: str, name: str, _dir: str = os.getcwd()):
    with open(f"{cut_dir(_dir)}\\{name}.txt", "w", encoding="utf-8") as file:
        file.write(text)


def audio_to_text(input_files: list[pathlib.Path], model: str = "tiny", _dir: str = f"{os.getcwd()}\\output"):
    whisper_model = whisper.load_model(model)

    for file in input_files:
        output_file_name = f"{file.stem.replace(' ', '_')}_{model}"
        result = whisper_model.transcribe(str(file), fp16=False)

        write_txt_file(
            text=edit_text(
                result['text'],
                count_words_in_line=10
            ),
            name=output_file_name, _dir=_dir
        )


def select_model():
    dict_models = {
        1: "tiny",
        2: "base",
        3: "small",
        4: "medium",
        5: "large"
    }

    while True:
        for i, v in dict_models.items():
            print(f"{i}: {v}")

        print("\nВведите номер модели || Enter the number of model")
        try:
            model_index = int(input("::: "))
            model = dict_models[model_index]

        except Exception:
            print("\nНеверный номер!!! || Invalid number!!!\n")
            continue

        print()
        return model


def main():
    audio_to_text(
        input_files=get_input_files(exts=["*.mp3"], _dir=f"{os.getcwd()}\\input"),
        model=select_model(), _dir=f"{os.getcwd()}\\output"
    )


if __name__ == '__main__':
    main()
