import json
import re
import argparse


class ParserError(Exception):
    """Исключение для синтаксических ошибок"""
    def __init__(self, error):
        super().__init__(error)


def parse_value(value, constants):
    """Парсит значение"""
    if isinstance(value, str):
        if value.startswith('?'):
            name = value[1:]
            if name in constants:
                return constants[name]
            raise ParserError(f"Constant '{name}' not defined")
        elif value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        else:
            try:
                return int(value)
            except ValueError:
                return value
    elif isinstance(value, list):
        return [parse_value(item, constants) for item in value]
    elif isinstance(value, dict):
        return {k: parse_value(v, constants) for k, v in value.items()}
    else:
        raise ParserError(f"Invalid value: '{value}'")


def parse_config(config_text, constants):
    """Парсит конфигурацию"""
    config = {}
    lines = config_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith('C') or line.startswith('<!--'):
            i += 1
            continue
        elif line.startswith('def'):
            match = re.match(r"def\s+(\w+)\s*=\s*(.*)", line)
            if match:
                name = match.group(1)
                value = match.group(2)
                constants[name] = parse_value(value, constants)
                i += 1
            else:
                raise ParserError(f"Invalid constant declaration: '{line}'")
        elif line.startswith('('):
            match = re.match(r"\(\s*\[(.*)\]\s*\)", line)
            if match:
                items = match.group(1).split(",")
                dictionary = {}
                for item in items:
                    item = item.strip()
                    match = re.match(r"(\w+)\s*:\s*(.*)", item)
                    if match:
                        key = match.group(1)
                        value = match.group(2)
                        dictionary[key] = parse_value(value, constants)
                    else:
                        raise ParserError(f"Invalid dictionary item: '{item}'")
                name = lines[i-1].strip()
                config[name] = dictionary
                i += 2
            else:
                raise ParserError(f"Invalid dictionary declaration: '{line}'")
        elif '{' in line:
            match = re.match(r"\{\s*(.*)\s*\}", line)
            if match:
                items = match.group(1).split(".")
                array = [parse_value(item.strip(), constants) for item in items]
                name = lines[i-1].strip()
                config[name] = array
                i += 2
            else:
                raise ParserError(f"Invalid array declaration: '{line}'")
        else:
            name = line
            value = lines[i + 1].strip()
            while i + 2 < len(lines) and not (lines[i + 2].strip().endswith(",") or lines[i + 2].strip().endswith(")") or lines[i + 2].strip().endswith("}")):
                value += '\n' + lines[i + 2].strip()
                i += 1
            config[name] = parse_value(value, constants)
            i += 2

        return config


def main():
    parser = argparse.ArgumentParser(description="Конвертер учебного конфигурационного языка.")
    parser.add_argument("input_file", help="Путь к входному файлу с конфигурацией в формате JSON.")
    parser.add_argument("output_file", help="Путь к выходному файлу с конфигурацией.")
    args = parser.parse_args()

    try:
        with open(args.input_file, "r") as f:
            config_json = json.load(f)
        constants = {}
        config_text = ""
        for key, value in config_json.items():
            constants[key] = parse_value(value, constants)
            config_text += f"{key}\n"
            config_text += f"def {key} = {value}\n"
        config = parse_config(config_text, constants)
        with open(args.output_file, "w") as f:
            for key, value in config.items():
                if isinstance(value, dict):
                    f.write(f"({key}:\n")
                    print(f"({key}:\n")
                    for inner_key, inner_value in value.items():
                        f.write(f"  {inner_key}: {inner_value},\n")
                        print(f"  {inner_key}: {inner_value},\n")
                    f.write(f"){key}\n")
                    print(f"){key}\n")
                elif isinstance(value, list):
                    f.write(f"{{ {value[0]}")
                    print(f"{{ {value[0]}")
                    for item in value[1:]:
                        f.write(f". {item}")
                        print(f". {item}")
                    f.write(f"}} {key}\n")
                    print(f"}} {key}\n")
                else:
                    f.write(f"{value} {key}\n")
                    print(f"{value} {key}\n")
    except FileNotFoundError:
        print(f"Ошибка: Файл '{args.input_file}' не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка: Файл '{args.input_file}' не является корректным JSON.")
    except ParserError as e:
        print(f"Ошибка парсинга: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()
