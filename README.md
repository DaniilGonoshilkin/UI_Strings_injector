# UI Strings injector

This script is used for auto-injection of product's UI strings into product's documentation.
When you have a task to localize both User Interface and Documentation for a particular application, you would eventually face the question: how to keep consistent translation between actual UI strings and their references in Documentation? There are diiferent ways to approach this problem, but from my experience working as a Localization Engineer, the best solution is to 'inject' the actual UI strings (from project's resource files) into Documentation files (in my case, Documentation is Online and represented as a number of HTML topics).

# General info

## File types

This script works if all UI strings of your project are contained within one or multiple JSON files and your Documentation is in form of one or multiple HTML files.

## File specifications

JSON files should be designed in a simple way, as a straight list of attributes and values, with no nestings and/or indentations. Encoding must be UTF-8 without BOM. Attribute names should be unique.
For HTML files, all the instances of UI strings in text (e.g. button names, section or tab titles) should be repleaced with placeholders <b>[[AttributeNameInJSONFile]]</b> (unique identifier from JSON file enclosed within double square brackets).

## How the script works

The script looks for placeholders in all HTML files within specified location and replaces them with actual UI strings from JSON files.
More specifically, the script identifies all JSON files with specified location, creates a unified dictionary data type in Python, then reads each HTML file subsequently in a loop. When a placeholder found in text, the script extracts uniqe ID (key) from the placeholder, search for this key in the dictionary and (if found) substitutes whole placeholder in HTML with a corresponding value, which is a required UI string.

## Languages

The script supports the following languages: Czech (cs-CZ), German (de-DE), French (fr-FR), English (en-US), Spanish (es-ES), Japanese (ja-JP), Brazil Portuguese (pt-BR), Russian (ru-RU), Simplified Chinese (zh-CN) and Traditional Chinese (zh-TW). The list is based on <b>lang_map</b> dictionary data type:
>
      # mapping dictionary to match names of HTML folders (keys) and names of JSON files (values)
      lang_map = {'cs-CZ': 'cs_CZ',
                  'de-DE': 'de_DE',
                  'fr-FR': 'fr_FR',
                  'en-US': 'en_US',
                  'es-ES': 'es_ES',
                  'ja-JP': 'ja_JP',
                  'pt-BR': 'pt_BR',
                  'ru-RU': 'ru_RU',
                  'zh-Hans': 'zh_CN',
                  'zh-Hant-TW': 'zh_TW'}

where keys are names of folders with HTML files and values are names of corresponding JSON files. So, technically, it is possible to add any other languages, simply by adding another pair of key/value into this dictionary.
<b>Please note however, that this script was not tested for compatibility with RTL languages.</b>

## Results

The script allows to achive the following results:
* increasing quality by keeping consistency between translations of strings in UI files and translations of the same strings in Documentation files
* saving time for translators and LQA engineers required to check translations of UI strings in Project Documentation
* reducing costs of translation, if placeholders have a specific mark up in a CAT-tool and excluded from wordcount for translation

# How to use

## 1. Clone the repository:

    git clone https://github.com/DaniilGonoshilkin/UI_Strings_injector.git

## 2. Dependencies: 

No external dependencies required to run the script

## 3. Run the script

Run the following command in Console

      python injector.py `<PATH TO JSON FILES>` `<PATH TO SOURCE FOLDER>` `<PATH TO TARGET FOLDER>`
