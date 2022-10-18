import os
import sys
import json
import codecs
import re
from distutils.dir_util import copy_tree, remove_tree


def strip_dictionary(dictionary):
    for key in dictionary.keys():
        dictionary[key] = re.sub(r'\s*\{\{.+?\}\}\s*', '', dictionary[key]) # strip angular expressions {{angular}}
        dictionary[key] = re.sub(r'[,;:.!\?]+$', '', dictionary[key]) # remove punctuation marks at the end of string
        dictionary[key] = re.sub(r'<br\s*[\/]?>', ' ', dictionary[key]) # replace <br/> tag on whitespace
        dictionary[key] = re.sub(r'<(?:.|\n)*?>', '', dictionary[key]) # strip tags
    return dictionary


def convert_to_dictionary(jsons):
    dictionary = {}
    for j in jsons:
        with codecs.open(j, 'r', 'utf-8') as json_file:
            try:
                data = json.load(json_file)
            except json.decoder.JSONDecodeError:
                print('\033[91m' + 'Error!' +
                      '\033[0m', 'Unexpected UTF-8 BOM. Check resource file encoding (must be UTF-8 without BOM)')
                continue
        dictionary.update(data)
    dictionary = strip_dictionary(dictionary)
    return dictionary


def identify_language(jsons, folder_path):
    """
    Identifies source folder language in order to use only necessary JSONs to create a dictionary
    Function returns list of JSON files for particular language
    """
    jsons_by_lang = []
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

    for key in lang_map.keys():
        if key in folder_path:
            print(key, 'language is detected for', folder_path)
            for j in jsons:
                if lang_map[key] in j:
                    jsons_by_lang.append(j)

    print('Following JSONs will be used:\n', '\n'.join(jsons_by_lang))
    return jsons_by_lang


def copy_files(src_path, tgt_path):
    print('Copying files from Source folder to Target...')
    copy_tree(src_path, tgt_path)


def iterate_folders(folder_path, list_of_f, flag):
    """
    Iterates through folder and returns a list of:
    * (if flag == 'F') files in the current folder and files in all subfolders
    OR
    * (if flag == 'D') folders (directories) only on the current level, without going through subfolders
    """
    if flag == 'F':
        dir_files = os.listdir(folder_path)
        full_paths = map(lambda name: os.path.join(folder_path, name), dir_files)
        for f in full_paths:
            if os.path.isfile(f):
                list_of_f.append(f)
            else:
                iterate_folders(f, list_of_f, flag='F')
        return list_of_f
    elif flag == 'D':
        dir_files = os.listdir(folder_path)
        full_paths = map(lambda name: os.path.join(folder_path, name), dir_files)
        for f in full_paths:
            if os.path.isdir(f):
                list_of_f.append(f)
        return list_of_f


def clean_target(tgt_path):
    file_list = []
    file_list = iterate_folders(tgt_path, file_list, flag='D')
    for f in file_list:
        remove_tree(f)
    print('Target folder cleared')

def strip_separator(m):
    """
    ***Specific case for a particular project only***
    Replaces '||' separator if used in a key (e.g. [[stringID||substringID]]) with '.'
    """
    split_key = m.group(1)
    split_key = split_key.split('||')
    new_key = '[[' + split_key[1] + '.' + split_key[0] + ']]'
    return new_key


def try_replace(m, dictionary, filename):
    try:
        return dictionary[m.group(1)]
    except KeyError:
        print('\033[93m' + 'Warning!' + '\033[0m', 'Key', m.group(0), 'is missing in file', filename)
        return m.group(0)


def inject_strings(html_files, dictionary):
    pattern = re.compile(r'\[\[([^\[\]]+)\]\]')
    separator_pattern = re.compile(r'\[\[([^\[\]]+\|\|[^\[\]]+)\]\]') # pattern for '||' separator
    for htm in html_files:
        if htm.endswith('all-in-one.htm') or not htm.endswith('.htm'):
            print(htm, 'skipped')
            continue
        with codecs.open(htm, 'r+', 'utf-8') as file:
            s = (file.read())
            pre_result = re.sub(separator_pattern, lambda m: strip_separator(m), s)
            result = re.sub(pattern, lambda m: try_replace(m, dictionary, htm), pre_result)
            file.seek(0)
            file.write(result)
            file.truncate()
            file.close()
            print('Completed processing file', htm)


if __name__ == "__main__":

    if len(sys.argv) < 4:
        sys.exit('Three arguments required: <PATH TO JSON FILES> <PATH TO SOURCE FOLDER> <PATH TO TARGET FOLDER>')

    os.system('color') # to support colored output in Windows console
    json_path = sys.argv[1]
    json_list = []
    json_list = iterate_folders(json_path, json_list, flag='F')
    print('JSON files found:\n', '\n'.join(json_list))

    source_path = sys.argv[2]
    target_path = sys.argv[3]
    clean_target(target_path)
    copy_files(source_path, target_path)
    folder_list = []
    folder_list = iterate_folders(target_path, folder_list, flag='D')
    for i in folder_list:
        print('\nStart processing folder:', i)
        htmls = []
        htmls = iterate_folders(i, htmls, flag='F')
        language_jsons = identify_language(json_list, i)
        jsons_dict = convert_to_dictionary(language_jsons)
        inject_strings(htmls, jsons_dict)
