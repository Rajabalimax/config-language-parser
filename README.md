# Парсер json в формат учебного конфигурационного языка

## Постановка задачи
Разработать инструмент командной строки для учебного конфигурационного языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.
Входной текст на языке json принимается из файла, путь к которому задан ключом командной строки. Выходной текст на учебном конфигурационном языке попадает в файл, путь к которому задан ключом командной строки.

Однострочные комментарии:
C Это однострочный комментарий

Многострочные комментарии:
\<!--
Это многострочный
комментарий
-->

Массивы:
{ значение. значение. значение. ... }

Словари:
([
 имя : значение,
 имя : значение,
 имя : значение,
 ...
])

Имена:
[a-zA-Z][_a-zA-Z0-9]*

Значения:
* Числа
* Массивы
* Словари
  
Объявление константы на этапе трансляции:
def имя = значение

Вычисление константы на этапе трансляции:
?(имя)

Результатом вычисления константного выражения является значение.

Все конструкции учебного конфигурационного языка (с учетом их возможной вложенности) должны быть покрыты тестами.

## Запуск программы
Запуск программы

![Запуск программы](https://github.com/Rajabalimax/config-language-parser/blob/main/1Con.png)
## Тестирование программы
Запуск тестов программы

![Запуск программы](https://github.com/Rajabalimax/config-language-parser/blob/main/2Con.png)
